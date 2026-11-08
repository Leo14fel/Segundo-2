package com.classforge.push;

import com.classforge.auth.persistence.*;
import com.classforge.auth.security.JwtService;
import com.classforge.notification.*;
import com.classforge.project.application.ProjectService;
import com.classforge.project.domain.document.*;
import com.classforge.project.persistence.ProjectMembershipEntity;
import com.classforge.project.persistence.ProjectMembershipRepository;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.*;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.support.TransactionTemplate;
import tools.jackson.databind.json.JsonMapper;
import java.net.URI;
import java.net.http.*;
import java.time.Instant;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT, properties = {
        "spring.mongodb.database=push_integration", "classforge.push.enabled=true", "classforge.push.public-key=test-public",
        "classforge.push.private-key=test-private", "classforge.push.subject=mailto:test@example.invalid", "classforge.push.poll-millis=3600000"
})
class PushIntegrationTests {
    @LocalServerPort int port;
    @Autowired UserRepository users;
    @Autowired JwtService jwt;
    @Autowired MongoTemplate mongo;
    @Autowired JsonMapper json;
    @Autowired ApplicationEventPublisher events;
    @Autowired PlatformTransactionManager transactions;
    @Autowired ProjectService projects;
    @Autowired ProjectMembershipRepository memberships;
    @Autowired PushDeliveryService deliveries;
    @MockitoBean VapidWebPushGateway gateway;
    final HttpClient http = HttpClient.newHttpClient();
    UserEntity user() { UUID id = UUID.randomUUID(); return users.save(new UserEntity(id, "Push QA", id + "@test.invalid", "unused", Instant.now())); }
    HttpResponse<String> request(UserEntity user, String method, String path, Object body) throws Exception {
        var request = HttpRequest.newBuilder(URI.create("http://localhost:" + port + "/api/push" + path));
        if (user != null) request.header("Authorization", "Bearer " + jwt.issue(user));
        request.header("Content-Type", "application/json").method(method, body == null ? HttpRequest.BodyPublishers.noBody() : HttpRequest.BodyPublishers.ofString(json.writeValueAsString(body)));
        return http.send(request.build(), HttpResponse.BodyHandlers.ofString());
    }
    String endpoint() { return "https://fcm.googleapis.com/fcm/send/" + UUID.randomUUID(); }
    Map<String,Object> subscription(String endpoint) {
        byte[] point = new byte[65]; point[0] = 4;
        return Map.of("endpoint", endpoint, "keys", Map.of("p256dh", Base64.getUrlEncoder().encodeToString(point), "auth", Base64.getUrlEncoder().encodeToString(new byte[16])));
    }
    @Test void requiresAuthenticationAndNeverExposesPrivateKey() throws Exception {
        int status = request(null, "GET", "/config", null).statusCode();
        assertTrue(status == 401 || status == 403);
        var response = request(user(), "GET", "/config", null);
        assertEquals(200, response.statusCode()); assertTrue(json.readTree(response.body()).get("enabled").asBoolean());
        assertFalse(response.body().contains("test-private"));
    }
    @Test void endpointOwnershipCannotBeReassignedOrDeletedByAnotherAccount() throws Exception {
        var owner = user(); var stranger = user(); String endpoint = endpoint(); String id = PushSubscriptionService.id(endpoint);
        assertEquals(200, request(owner, "POST", "/subscriptions", subscription(endpoint)).statusCode());
        assertEquals(409, request(stranger, "POST", "/subscriptions", subscription(endpoint)).statusCode());
        assertEquals(200, request(stranger, "DELETE", "/subscriptions", Map.of("endpoint", endpoint)).statusCode());
        assertEquals(owner.getId(), mongo.findById(id, PushSubscription.class).userId());
        assertEquals(200, request(owner, "DELETE", "/subscriptions", Map.of("endpoint", endpoint)).statusCode());
        assertNull(mongo.findById(id, PushSubscription.class)); verifyNoInteractions(gateway);
    }
    @Test void queueIsAtomicIdempotentAndUsesBsonDateForTtl() throws Exception {
        var owner = user(); String endpoint = endpoint();
        assertEquals(200, request(owner, "POST", "/subscriptions", subscription(endpoint)).statusCode());
        UUID id = UUID.randomUUID();
        var notification = new ProjectNotification(id, UUID.randomUUID(), owner.getId(), ProjectNotification.Type.PROJECT_ACTIVITY,
                "Private title", "Private diagram", null, null, id.toString(), false, Instant.now(), null);
        var event = new ProjectNotificationEvent(owner.getId(), "NOTIFICATION_CREATED", notification);
        var tx = new TransactionTemplate(transactions);
        var query = Query.query(Criteria.where("notificationId").is(id));
        tx.executeWithoutResult(status -> { events.publishEvent(event); status.setRollbackOnly(); });
        assertEquals(0, mongo.count(query, PushDelivery.class));
        tx.executeWithoutResult(status -> { events.publishEvent(event); events.publishEvent(event); });
        assertEquals(1, mongo.count(query, PushDelivery.class));
        var job = mongo.findOne(query, PushDelivery.class);
        var raw = mongo.getCollection("push_deliveries").find(new org.bson.Document("_id", job.id())).first();
        assertInstanceOf(Date.class, raw.get("expiresAt"));
        assertEquals("PENDING", job.status()); verifyNoInteractions(gateway);
        request(owner, "DELETE", "/subscriptions", Map.of("endpoint", endpoint));
        assertEquals(0, mongo.count(query, PushDelivery.class));
    }
    @Test void diagramChangeQueuesOtherMembersAndWorkerDeliversAfterCommit() throws Exception {
        var owner = user(); var editor = user();
        var project = projects.create(owner.getId(), "Push integration");
        memberships.save(ProjectMembershipEntity.editor(project.id(), editor.getId()));
        String endpoint = endpoint();
        assertEquals(200, request(editor, "POST", "/subscriptions", subscription(endpoint)).statusCode());
        var diagram = new ProjectDocument("1.0", new UmlModel(List.of(new UmlClass(UUID.randomUUID(), "Libro", List.of())), List.of()), DiagramLayout.empty());
        projects.saveDocument(owner.getId(), project.id(), 0, diagram);
        var query = Query.query(Criteria.where("projectId").is(project.id()));
        assertEquals(1, mongo.count(query, PushDelivery.class));
        var job = mongo.findOne(query, PushDelivery.class);
        assertEquals(editor.getId(), job.userId());
        assertNotNull(mongo.findById(job.notificationId(), ProjectNotification.class));
        verifyNoInteractions(gateway);
        when(gateway.send(any(), any())).thenReturn(201);
        deliveries.drain();
        assertEquals("SENT", mongo.findById(job.id(), PushDelivery.class).status());
        verify(gateway).send(argThat(sub -> sub.userId().equals(editor.getId())), any());
        request(editor, "DELETE", "/subscriptions", Map.of("endpoint", endpoint));
    }
}
