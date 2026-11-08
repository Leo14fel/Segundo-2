package com.classforge.push;

import org.junit.jupiter.api.Test;
import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.security.*;
import java.security.interfaces.*;
import java.security.spec.ECGenParameterSpec;
import java.time.Instant;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;

class VapidWebPushGatewayTests {
    KeyPair pair() throws Exception {
        var generator = KeyPairGenerator.getInstance("EC");
        generator.initialize(new ECGenParameterSpec("secp256r1"));
        return generator.generateKeyPair();
    }
    byte[] coordinate(BigInteger value) {
        byte[] raw = value.toByteArray(), fixed = new byte[32];
        int length = Math.min(raw.length, 32);
        System.arraycopy(raw, raw.length - length, fixed, 32 - length, length);
        return fixed;
    }
    String publicKey(KeyPair pair) {
        var point = ((ECPublicKey)pair.getPublic()).getW();
        byte[] raw = new byte[65]; raw[0] = 4;
        System.arraycopy(coordinate(point.getAffineX()), 0, raw, 1, 32);
        System.arraycopy(coordinate(point.getAffineY()), 0, raw, 33, 32);
        return Base64.getUrlEncoder().withoutPadding().encodeToString(raw);
    }
    @Test void generatesEncryptedPayloadAndVapidHeadersWithoutNetwork() throws Exception {
        var application = pair(); var device = pair();
        var settings = new PushSettings(true, publicKey(application),
                Base64.getUrlEncoder().withoutPadding().encodeToString(coordinate(((ECPrivateKey)application.getPrivate()).getS())),
                "mailto:test@example.invalid", "fcm.googleapis.com");
        byte[] secret = new byte[16]; new SecureRandom().nextBytes(secret);
        var subscription = new PushSubscription("id", UUID.randomUUID(), "https://fcm.googleapis.com/fcm/send/test",
                publicKey(device), Base64.getUrlEncoder().withoutPadding().encodeToString(secret), Instant.now(), Instant.now());
        String message = "Private notification payload";
        var gateway = new VapidWebPushGateway(settings, new PushEndpointPolicy(settings));
        var request = gateway.encrypt(subscription, message.getBytes(StandardCharsets.UTF_8));
        assertEquals("aes128gcm", request.getHeaders().get("Content-Encoding"));
        assertTrue(request.getHeaders().get("Authorization").startsWith("vapid "));
        assertTrue(request.getBody().length > message.length());
        assertFalse(new String(request.getBody(), StandardCharsets.ISO_8859_1).contains(message));
    }
    @Test void disabledGatewayRequiresNoKeysAndCannotSend() {
        var settings = new PushSettings(false, "", "", "", "fcm.googleapis.com");
        var gateway = new VapidWebPushGateway(settings, new PushEndpointPolicy(settings));
        assertThrows(IllegalStateException.class, () -> gateway.encrypt(null, new byte[0]));
    }
}
