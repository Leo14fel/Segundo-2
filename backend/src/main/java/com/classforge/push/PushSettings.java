package com.classforge.push;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
@Component
public record PushSettings(
 @Value("${classforge.push.enabled:false}") boolean enabled,
 @Value("${classforge.push.public-key:}") String publicKey,
 @Value("${classforge.push.private-key:}") String privateKey,
 @Value("${classforge.push.subject:}") String subject,
 @Value("${classforge.push.allowed-hosts:fcm.googleapis.com,updates.push.services.mozilla.com,web.push.apple.com}") String allowedHosts
) { @Override public String toString(){return "PushSettings[enabled="+enabled+", privateKey=REDACTED]";} }
