package com.classforge.push;

import org.junit.jupiter.api.*;
import org.mockito.ArgumentCaptor;
import org.springframework.data.mongodb.core.*;
import org.springframework.data.mongodb.core.query.*;
import tools.jackson.databind.json.JsonMapper;
import java.time.*;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
import static org.mockito.ArgumentMatchers.*;

class PushDeliveryServiceTests {
    final MongoTemplate mongo = mock(MongoTemplate.class);
    final WebPushGateway gateway = mock(WebPushGateway.class);
    final Instant now = Instant.parse("2026-11-08T12:00:00Z");
    final UUID user = UUID.randomUUID(), project = UUID.randomUUID(), notification = UUID.randomUUID();
    final PushSettings settings = new PushSettings(true, "pub", "priv", "mailto:a@b.invalid", "fcm.googleapis.com");
    final PushSubscription subscription = new PushSubscription("sub", user, "https://fcm.googleapis.com/send/a", "key", "auth", now, now);
    final PushDeliveryService service = new PushDeliveryService(mongo, settings, gateway, Clock.fixed(now, ZoneOffset.UTC), JsonMapper.builder().build());

    void claim(int attempts) {
        var job = new PushDelivery("job", "sub", user, project, notification, "PENDING", attempts, now, now.plusSeconds(30), Date.from(now.plusSeconds(3600)));
        when(mongo.findAndModify(any(Query.class), any(Update.class), any(FindAndModifyOptions.class), eq(PushDelivery.class))).thenReturn(job, (PushDelivery)null);
        when(mongo.findById("sub", PushSubscription.class)).thenReturn(subscription);
    }
    Update update() {
        var capture = ArgumentCaptor.forClass(Update.class);
        verify(mongo).updateFirst(any(Query.class), capture.capture(), eq(PushDelivery.class));
        return capture.getValue();
    }
    Object set(String key) { return update().getUpdateObject().get("$set", org.bson.Document.class).get(key); }
    @AfterEach void stop() { service.close(); }

    @Test void successfulSendFinishesJobAndContainsOnlyGenericContent() throws Exception {
        claim(1); when(gateway.send(eq(subscription), any())).thenReturn(201);
        service.drain();
        assertEquals("SENT", set("status"));
        var payload = ArgumentCaptor.forClass(byte[].class);
        verify(gateway).send(eq(subscription), payload.capture());
        var data = JsonMapper.builder().build().readTree(payload.getValue());
        assertEquals(user.toString(), data.get("recipientUserId").asString());
        assertEquals("/?project=" + project + "&view=activity", data.get("url").asString());
        assertEquals(5, data.size());
        assertFalse(new String(payload.getValue(), java.nio.charset.StandardCharsets.UTF_8).contains(subscription.endpoint()));
    }
    @Test void expiredEndpointIsRemovedWithoutRetrying() throws Exception {
        claim(1); when(gateway.send(eq(subscription), any())).thenReturn(410);
        service.drain(); assertEquals("DEAD", set("status"));
        var query = ArgumentCaptor.forClass(Query.class);
        verify(mongo).remove(query.capture(), eq(PushSubscription.class));
        assertEquals(user, query.getValue().getQueryObject().get("userId"));
    }
    @Test void providerFailureSchedulesRetryInsteadOfLosingJob() throws Exception {
        claim(1); when(gateway.send(eq(subscription), any())).thenReturn(503);
        service.drain(); assertEquals(now.plusSeconds(20), set("nextAttemptAt"));
    }
    @Test void networkExceptionRetriesAndEventuallyStops() throws Exception {
        claim(8); when(gateway.send(eq(subscription), any())).thenThrow(new java.io.IOException("network"));
        service.drain(); assertEquals("DEAD", set("status"));
    }
    @Test void reassignedDeviceNeverReceivesAnotherUsersNotification() {
        claim(1);
        when(mongo.findById("sub", PushSubscription.class)).thenReturn(new PushSubscription("sub", UUID.randomUUID(), subscription.endpoint(), "key", "auth", now, now));
        service.drain(); assertEquals("DEAD", set("status")); verifyNoInteractions(gateway);
    }
    @Test void disabledPushDoesNotTouchDatabaseOrNetwork() {
        try(var disabled = new DisabledService(mongo, gateway, now)) { disabled.service.drain(); }
        verifyNoInteractions(mongo, gateway);
    }
    static class DisabledService implements AutoCloseable {
        final PushDeliveryService service;
        DisabledService(MongoTemplate mongo, WebPushGateway gateway, Instant now) {
            service = new PushDeliveryService(mongo, new PushSettings(false, "", "", "", ""), gateway, Clock.fixed(now, ZoneOffset.UTC), JsonMapper.builder().build());
        }
        public void close() { service.close(); }
    }
}
