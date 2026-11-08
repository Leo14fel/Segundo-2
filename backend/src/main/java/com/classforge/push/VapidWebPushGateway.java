package com.classforge.push;
import nl.martijndwars.webpush.*;
import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.springframework.stereotype.Component;
import java.net.http.*;
import java.security.Security;
import java.time.Duration;
import java.util.*;
@Component
public class VapidWebPushGateway implements WebPushGateway {
 private final PreparedPushService service;
 private final PushEndpointPolicy policy;
 private final HttpClient client=HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(5)).followRedirects(HttpClient.Redirect.NEVER).build();
 public VapidWebPushGateway(PushSettings settings,PushEndpointPolicy policy){this.policy=policy;
  if(!settings.enabled()){service=null;return;}
  if(settings.publicKey().isBlank()||settings.privateKey().isBlank()||settings.subject().isBlank())throw new IllegalStateException("Push activo requiere claves VAPID y subject configurados fuera del código.");
  try{if(Security.getProvider("BC")==null)Security.addProvider(new BouncyCastleProvider());service=new PreparedPushService(settings.publicKey(),settings.privateKey(),settings.subject());}
  catch(Exception e){throw new IllegalStateException("No se pudieron cargar las claves VAPID configuradas.");}
 }
 @Override public int send(PushSubscription subscription,byte[] payload)throws Exception{
  if(service==null)throw new IllegalStateException("Web Push está desactivado.");
  var uri=policy.validate(subscription.endpoint());
  var encrypted=encrypt(subscription,payload);
  var request=java.net.http.HttpRequest.newBuilder(uri).timeout(Duration.ofSeconds(8));
  for(var h:encrypted.getHeaders().entrySet())if(!Set.of("content-length","host","connection","expect").contains(h.getKey().toLowerCase(Locale.ROOT)))request.header(h.getKey(),h.getValue());
  var body=encrypted.getBody();
  return client.send(request.POST(java.net.http.HttpRequest.BodyPublishers.ofByteArray(body)).build(),HttpResponse.BodyHandlers.discarding()).statusCode();
 }
 nl.martijndwars.webpush.HttpRequest encrypt(PushSubscription subscription,byte[] payload)throws Exception{
  if(service==null)throw new IllegalStateException("Web Push está desactivado.");
  policy.validate(subscription.endpoint());
  return service.prepare(new Notification(subscription.endpoint(),subscription.p256dh(),subscription.auth(),payload,3600));
 }
 private static final class PreparedPushService extends AbstractPushService<PreparedPushService> {
  PreparedPushService(String publicKey,String privateKey,String subject)throws java.security.GeneralSecurityException{super(publicKey,privateKey,subject);}
  nl.martijndwars.webpush.HttpRequest prepare(Notification notification)throws Exception{return prepareRequest(notification,Encoding.AES128GCM);}
 }

}
