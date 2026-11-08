package com.classforge.push;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import java.time.Instant;
import java.util.UUID;
import java.util.Date;
@Document("push_deliveries")
public record PushDelivery(@Id String id, String subscriptionId, UUID userId, UUID projectId, UUID notificationId,
 String status, int attempts, Instant nextAttemptAt, Instant leaseUntil, Date expiresAt) {}
