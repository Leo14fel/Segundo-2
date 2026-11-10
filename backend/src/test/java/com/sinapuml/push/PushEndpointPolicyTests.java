package com.sinapuml.push;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.springframework.web.server.ResponseStatusException;
import java.util.Base64;
import static org.junit.jupiter.api.Assertions.*;

class PushEndpointPolicyTests {
    final PushSettings settings = new PushSettings(true, "public", "private-secret", "mailto:test@example.invalid",
            "fcm.googleapis.com,updates.push.services.mozilla.com,web.push.apple.com");
    final PushEndpointPolicy policy = new PushEndpointPolicy(settings);

    @ParameterizedTest @ValueSource(strings = {
            "http://fcm.googleapis.com/send/abc", "https://127.0.0.1/internal", "https://localhost/internal",
            "https://fcm.googleapis.com.attacker.invalid/send", "https://user@fcm.googleapis.com/send",
            "https://fcm.googleapis.com:8443/send", "https://fcm.googleapis.com/send#fragment", "not-a-url"
    })
    void rejectsUntrustedDestinations(String endpoint) {
        assertThrows(ResponseStatusException.class, () -> policy.validate(endpoint));
    }

    @ParameterizedTest @ValueSource(strings = {
            "https://fcm.googleapis.com/fcm/send/abc", "https://updates.push.services.mozilla.com/wpush/v2/abc",
            "https://web.push.apple.com/Qabc", "https://fcm.googleapis.com:443/send"
    })
    void acceptsKnownHttpsProviders(String endpoint) { assertEquals("https", policy.validate(endpoint).getScheme()); }

    @Test void rejectsMalformedSubscriptionKeysAndRedactsConfiguration() {
        assertThrows(ResponseStatusException.class, () -> policy.keys("bad", "bad"));
        byte[] point = new byte[65]; point[0] = 4;
        String key = Base64.getUrlEncoder().withoutPadding().encodeToString(point);
        assertThrows(ResponseStatusException.class, () -> policy.keys(key, "short"));
        assertDoesNotThrow(() -> policy.keys(key, Base64.getUrlEncoder().encodeToString(new byte[16])));
        assertFalse(settings.toString().contains("private-secret"));
    }
}
