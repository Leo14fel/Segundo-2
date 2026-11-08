package com.classforge.push;
import org.springframework.stereotype.Component;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;
import java.net.URI;
import java.util.*;
@Component
public class PushEndpointPolicy {
 private final Set<String> hosts;
 public PushEndpointPolicy(PushSettings settings){hosts=new HashSet<>();for(String h:settings.allowedHosts().split(","))if(!h.isBlank())hosts.add(h.trim().toLowerCase(Locale.ROOT));}
 public URI validate(String endpoint){
  try{if(endpoint==null||endpoint.length()>4096)throw new IllegalArgumentException();URI uri=URI.create(endpoint);String host=uri.getHost();
   if(!"https".equalsIgnoreCase(uri.getScheme())||host==null||!hosts.contains(host.toLowerCase(Locale.ROOT))||uri.getUserInfo()!=null||uri.getFragment()!=null||uri.getPort()!=-1&&uri.getPort()!=443||uri.getPath()==null||uri.getPath().isBlank())throw new IllegalArgumentException();return uri;
  }catch(IllegalArgumentException e){throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"El endpoint push no pertenece a un proveedor HTTPS permitido.");}
 }
 public void keys(String publicKey,String auth){try{byte[] point=Base64.getUrlDecoder().decode(publicKey),secret=Base64.getUrlDecoder().decode(auth);if(point.length!=65||point[0]!=4||secret.length!=16)throw new IllegalArgumentException();}catch(RuntimeException e){throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Las claves de suscripción push son inválidas.");}}
}
