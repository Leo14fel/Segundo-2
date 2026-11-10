package com.sinapuml.push;
import com.sinapuml.auth.security.CurrentUser;
import jakarta.validation.Valid;
import jakarta.validation.constraints.*;
import org.springframework.web.bind.annotation.*;
import java.util.Map;
@RestController
@RequestMapping("/api/push")
public class PushController {
 private final PushSettings settings;private final PushSubscriptionService subscriptions;private final CurrentUser user;
 public PushController(PushSettings settings,PushSubscriptionService subscriptions,CurrentUser user){this.settings=settings;this.subscriptions=subscriptions;this.user=user;}
 @GetMapping("/config") public Map<String,Object> config(){return Map.of("enabled",settings.enabled(),"publicKey",settings.enabled()?settings.publicKey():"");}
 @PostMapping("/subscriptions") public Map<String,String> subscribe(@Valid @RequestBody SubscriptionRequest input){return Map.of("id",subscriptions.subscribe(user.id(),input.endpoint(),input.keys().p256dh(),input.keys().auth()));}
 @DeleteMapping("/subscriptions") public void unsubscribe(@Valid @RequestBody EndpointRequest input){subscriptions.unsubscribe(user.id(),input.endpoint());}
 public record Keys(@NotBlank @Size(max=128) String p256dh,@NotBlank @Size(max=128) String auth){}
 public record SubscriptionRequest(@NotBlank @Size(max=4096) String endpoint,@NotNull @Valid Keys keys){}
 public record EndpointRequest(@NotBlank @Size(max=4096) String endpoint){}
}
