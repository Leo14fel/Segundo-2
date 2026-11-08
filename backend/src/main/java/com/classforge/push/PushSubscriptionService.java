package com.classforge.push;
import org.springframework.stereotype.Service;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.*;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.time.Instant;
import java.util.*;
@Service
public class PushSubscriptionService {
 private final MongoTemplate mongo;private final PushEndpointPolicy policy;private final PushSettings settings;
 public PushSubscriptionService(MongoTemplate mongo,PushEndpointPolicy policy,PushSettings settings){this.mongo=mongo;this.policy=policy;this.settings=settings;}
 public String subscribe(UUID user,String endpoint,String p256dh,String auth){
  if(!settings.enabled())throw new ResponseStatusException(HttpStatus.SERVICE_UNAVAILABLE,"Push todavía no está configurado en el servidor.");
  policy.validate(endpoint);policy.keys(p256dh,auth);String id=id(endpoint);var old=mongo.findById(id,PushSubscription.class);Instant now=Instant.now();
  if(old!=null&&!old.userId().equals(user))throw new ResponseStatusException(HttpStatus.CONFLICT,"Este dispositivo sigue vinculado a otra cuenta. Renueva la suscripción del navegador.");
  if(old==null){if(mongo.count(Query.query(Criteria.where("userId").is(user)),PushSubscription.class)>=10)throw new ResponseStatusException(HttpStatus.CONFLICT,"Alcanzaste el máximo de 10 dispositivos; desactiva uno antes de agregar otro.");
   try{mongo.insert(new PushSubscription(id,user,endpoint,p256dh,auth,now,now));}catch(org.springframework.dao.DuplicateKeyException collision){throw new ResponseStatusException(HttpStatus.CONFLICT,"La suscripción cambió. Intenta activarla nuevamente.");}
  }else mongo.updateFirst(Query.query(Criteria.where("id").is(id).and("userId").is(user)),new Update().set("p256dh",p256dh).set("auth",auth).set("updatedAt",now),PushSubscription.class);
  return id;
 }
 public void unsubscribe(UUID user,String endpoint){if(endpoint==null||endpoint.length()>4096)throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Endpoint inválido.");String id=id(endpoint);mongo.remove(Query.query(Criteria.where("id").is(id).and("userId").is(user)),PushSubscription.class);mongo.remove(Query.query(Criteria.where("subscriptionId").is(id).and("userId").is(user)),PushDelivery.class);}
 static String id(String value){try{return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(value.getBytes(StandardCharsets.UTF_8)));}catch(Exception e){throw new IllegalStateException(e);}}
}
