package com.classforge.push;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import java.time.Instant;
import java.util.UUID;
@Document("push_subscriptions")
public record PushSubscription(@Id String id, UUID userId, String endpoint, String p256dh, String auth, Instant createdAt, Instant updatedAt) { @Override public String toString(){return "PushSubscription[id="+id+", userId="+userId+"]";} }
