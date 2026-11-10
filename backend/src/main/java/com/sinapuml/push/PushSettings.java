package com.sinapuml.push;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
@Component
public record PushSettings(
 @Value("${sinapuml.push.enabled:false}") boolean enabled,
 @Value("${sinapuml.push.public-key:}") String publicKey,
 @Value("${sinapuml.push.private-key:}") String privateKey,
 @Value("${sinapuml.push.subject:}") String subject,
 @Value("${sinapuml.push.allowed-hosts:fcm.googleapis.com,updates.push.services.mozilla.com,web.push.apple.com}") String allowedHosts
) { @Override public String toString(){return "PushSettings[enabled="+enabled+", privateKey=REDACTED]";} }
