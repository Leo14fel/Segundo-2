package com.classforge.push;

import com.classforge.notification.ProjectNotificationEvent;
import jakarta.annotation.PreDestroy;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.event.EventListener;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.core.*;
import org.springframework.data.mongodb.core.query.*;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.*;
import tools.jackson.databind.json.JsonMapper;
import java.time.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicBoolean;

/** Persist intent in the notification transaction; do network I/O on a separate worker. */
@Service
public class PushDeliveryService {
 private final MongoTemplate mongo;private final PushSettings settings;private final WebPushGateway gateway;private final Clock clock;private final JsonMapper json;
 private final AtomicBoolean running=new AtomicBoolean();
 private final ExecutorService worker=Executors.newSingleThreadExecutor(task->{Thread t=new Thread(task,"classforge-push-delivery");t.setDaemon(true);return t;});
 public PushDeliveryService(MongoTemplate mongo,PushSettings settings,WebPushGateway gateway,@Qualifier("projectActivityClock") Clock clock,JsonMapper json){this.mongo=mongo;this.settings=settings;this.gateway=gateway;this.clock=clock;this.json=json;}
 @EventListener
 @Transactional(propagation=Propagation.MANDATORY)
 public void queue(ProjectNotificationEvent event){
  if(!settings.enabled()||!"NOTIFICATION_CREATED".equals(event.type())||event.notification()==null)return;
  Instant now=clock.instant();
  var subscriptions=mongo.find(Query.query(Criteria.where("userId").is(event.recipientUserId())),PushSubscription.class);
  for(var subscription:subscriptions){String id=PushSubscriptionService.id(event.notification().id()+":"+subscription.id());
   var update=new Update().setOnInsert("subscriptionId",subscription.id()).setOnInsert("userId",event.recipientUserId()).setOnInsert("projectId",event.notification().projectId()).setOnInsert("notificationId",event.notification().id()).setOnInsert("status","PENDING").setOnInsert("attempts",0).setOnInsert("nextAttemptAt",now).setOnInsert("leaseUntil",Instant.EPOCH).setOnInsert("expiresAt",Date.from(now.plus(Duration.ofDays(7))));
   try{mongo.upsert(Query.query(Criteria.where("id").is(id)),update,PushDelivery.class);}catch(org.springframework.dao.DuplicateKeyException concurrent){/* deterministic ID: the other insert is the same job */}
  }
 }
 @Scheduled(fixedDelayString="${classforge.push.poll-millis:5000}",initialDelayString="${classforge.push.poll-millis:5000}")
 public void schedule(){if(!settings.enabled()||!running.compareAndSet(false,true))return;try{worker.submit(()->{try{drain();}finally{running.set(false);}});}catch(RejectedExecutionException stopped){running.set(false);}}
 public void drain(){
  if(!settings.enabled())return;
  for(int i=0;i<20&&!Thread.currentThread().isInterrupted();i++){
   Instant now=clock.instant();
   var query=Query.query(Criteria.where("status").is("PENDING").and("nextAttemptAt").lte(now).and("leaseUntil").lte(now).and("expiresAt").gt(Date.from(now))).with(Sort.by("nextAttemptAt"));
   var job=mongo.findAndModify(query,new Update().set("leaseUntil",now.plusSeconds(30)).inc("attempts",1),FindAndModifyOptions.options().returnNew(true),PushDelivery.class);
   if(job==null)return;
   deliver(job);
  }
 }
 private void deliver(PushDelivery job){
  var subscription=mongo.findById(job.subscriptionId(),PushSubscription.class);
  if(subscription==null||!subscription.userId().equals(job.userId())){finish(job,"DEAD");return;}
  try{
   // Keep diagram content, names, chat and tokens off lock screens and transport payloads.
   byte[] payload=json.writeValueAsBytes(Map.of("title","Forge Studio","body","Tienes novedades en un proyecto compartido.","tag",job.notificationId().toString(),"recipientUserId",job.userId().toString(),"url","/?project="+job.projectId()+"&view=activity"));
   int status=gateway.send(subscription,payload);
   if(status>=200&&status<300){finish(job,"SENT");return;}
   if(status==404||status==410){mongo.remove(Query.query(Criteria.where("id").is(subscription.id()).and("userId").is(job.userId())),PushSubscription.class);finish(job,"DEAD");return;}
   retry(job);
  }catch(InterruptedException interrupted){Thread.currentThread().interrupt();retry(job);}catch(Exception failure){retry(job);}
 }
 private void finish(PushDelivery job,String status){mongo.updateFirst(Query.query(Criteria.where("id").is(job.id())),new Update().set("status",status).set("leaseUntil",Instant.EPOCH),PushDelivery.class);}
 private void retry(PushDelivery job){if(job.attempts()>=8){finish(job,"DEAD");return;}long delay=Math.min(3600,10L<<Math.min(job.attempts(),8));mongo.updateFirst(Query.query(Criteria.where("id").is(job.id())),new Update().set("nextAttemptAt",clock.instant().plusSeconds(delay)).set("leaseUntil",Instant.EPOCH),PushDelivery.class);}
 @PreDestroy public void close(){worker.shutdownNow();}
}
