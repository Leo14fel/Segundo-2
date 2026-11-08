package com.classforge.assistant;

import com.classforge.project.domain.document.*;
import tools.jackson.databind.JsonNode;
import java.text.Normalizer;
import java.util.*;
import java.util.regex.Pattern;

/** Ground each method edit against the request and the authoritative document. */
public final class AssistantOperationSupport {
 private AssistantOperationSupport() {}
 public static String label(UmlClass owner,UmlOperation op){return owner.name()+"."+signature(op);}
 public static String signature(UmlOperation op){return op.name()+"("+String.join(",",op.parameters().stream().map(UmlParameter::type).toList())+")";}
 public static AssistantOperationEdit arguments(JsonNode args,UmlClass owner){
  String change=text(args,"change",true).toUpperCase(Locale.ROOT);if(!Set.of("CREATE","UPDATE","DELETE").contains(change))throw fail("Cambio de método desconocido.");
  UmlOperation existing=null;String reference=text(args,"existing_operation_ref",false);
  if(!change.equals("CREATE"))existing=owner.operations().stream().filter(op->label(owner,op).equals(reference)).findFirst().orElseThrow(()->fail("Selecciona una firma existente en la clase indicada."));
  else if(reference!=null)throw fail("CREATE no puede seleccionar un método existente.");
  String name=text(args,"name",false),returnType=text(args,"return_type",false);UmlVisibility visibility=null;
  String visible=text(args,"visibility",false);if(visible!=null)try{visibility=UmlVisibility.valueOf(visible.toUpperCase(Locale.ROOT));}catch(IllegalArgumentException e){throw fail("Visibilidad de método inválida.");}
  List<UmlParameter> parameters=null;JsonNode values=args.get("parameters");
  if(values!=null&&!values.isNull()){
   if(!values.isArray()||values.size()>20)throw fail("Los parámetros deben ser una lista de hasta 20 elementos.");
   parameters=new ArrayList<>();for(JsonNode p:values){String pn=text(p,"name",true),pt=text(p,"type",true);UUID id=UUID.randomUUID();if(existing!=null){var matches=existing.parameters().stream().filter(old->old.name().equals(pn)).toList();if(matches.size()==1)id=matches.getFirst().id();}parameters.add(new UmlParameter(id,pn,pt));}
  }
  if(change.equals("CREATE")&&name==null)throw fail("Indica el nombre del método nuevo.");
  if(change.equals("DELETE")&&(name!=null||returnType!=null||visibility!=null||parameters!=null))throw fail("DELETE no admite modificaciones de propiedades.");
  if(change.equals("UPDATE")&&name==null&&returnType==null&&visibility==null&&parameters==null)throw fail("No se indicó qué propiedad del método cambiar.");
  return new AssistantOperationEdit(change,existing==null?null:existing.id(),name,returnType,visibility,parameters);
 }
 public static void singleRequest(String userText){
  String value=normalize(userText);
  if(Pattern.compile("\\b(metodos|operaciones|methods|operations)\\b").matcher(value).find()
     ||Pattern.compile("\\b(y|and|luego|despues)\\s+(?:tambien\\s+)?(agrega|anade|crea|elimina|borra|quita|renombra|modifica|actualiza|cambia|add|create|update|delete|remove|rename)\\b").matcher(value).find())
    throw fail("Solicita un solo cambio de método por petición; separa las otras acciones.");
 }
 public static void ground(String userText,AssistantPlanAction action,ProjectDocument document){
  singleRequest(userText);
  var edit=action.operationEdit();if(edit==null)throw fail("Falta la edición de método.");
  var owner=document.umlModel().classes().stream().filter(c->c.name().equals(action.className())).findFirst().orElseThrow(()->fail("La clase seleccionada no existe."));
  if(!mentions(userText,owner.name()))throw fail("Indica explícitamente la clase del método.");
  String text=normalize(userText);String mode=edit.change();
  if(mode==null||!Set.of("CREATE","UPDATE","DELETE").contains(mode))throw fail("Cambio de método inválido.");
  String verbs=mode.equals("CREATE")?"agrega|agregar|anade|anadir|crea|crear|add|create":mode.equals("DELETE")?"elimina|eliminar|borra|borrar|quita|quitar|delete|remove":"modifica|modificar|actualiza|actualizar|cambia|cambiar|renombra|renombrar|update|rename|change";
  if(!Pattern.compile("\\b("+verbs+")\\b").matcher(text).find())throw fail("La operación elegida no corresponde a la intención explícita del usuario.");
  if(mode.equals("DELETE")&&!Pattern.compile("\\b(elimina|eliminar|borra|borrar|quita|quitar|delete|remove)\\s+(?:(?:el|un|the)\\s+)?(?:metodo|operacion|method|operation)\\b").matcher(text).find())throw fail("Para eliminar un método solicita explícitamente eliminar el método completo.");
  UmlOperation old=null;
  if(!mode.equals("CREATE")){
   old=owner.operations().stream().filter(op->op.id().equals(edit.operationId())).findFirst().orElseThrow(()->fail("El método seleccionado no existe."));
   if(!mentions(userText,old.name()))throw fail("Indica el método que quieres modificar.");
   final String selectedName=old.name();
   if(owner.operations().stream().filter(op->op.name().equals(selectedName)).count()>1&&!text.replaceAll("\\s+","").contains(normalize(signature(old)).replaceAll("\\s+","")))throw fail("Hay sobrecargas. Indica la firma completa, por ejemplo "+signature(old)+".");
  }
  if(edit.name()!=null&&!mentions(userText,edit.name()))throw fail("El nombre del método no está en la petición.");
  if(edit.returnType()!=null){
   if(!Pattern.compile("\\b(retorno|devuelva|devuelve|devolver|retorna|retorne|return|returns)\\b").matcher(text).find())throw fail("Indica el retorno explícitamente, por ejemplo 'retorno BOOLEAN'.");
   typeInRequest(userText,edit.returnType());
  }
  if(edit.visibility()!=null){String[] words=switch(edit.visibility()){case PUBLIC->new String[]{"public","publico","publica"};case PRIVATE->new String[]{"private","privado","privada"};case PROTECTED->new String[]{"protected","protegido","protegida"};case PACKAGE->new String[]{"package","paquete"};};if(Arrays.stream(words).noneMatch(w->mentions(userText,w)))throw fail("La visibilidad propuesta no fue solicitada.");}
  if(edit.parameters()!=null){
   if(edit.parameters().isEmpty()&&!mode.equals("CREATE")&&!text.matches("(?s).*(sin parametros|sin argumentos|no parameters|no arguments).*"))throw fail("Para vaciar parámetros indica explícitamente 'sin parámetros'.");
   if(old!=null){
    for(var previous:old.parameters()){
     boolean retained=edit.parameters().stream().anyMatch(p->p.id().equals(previous.id()));
     if(!retained&&!text.matches("(?s).*(sin parametros|sin argumentos|reemplaza todos los parametros|reemplazar todos los parametros).*")){
      boolean removalCue=Pattern.compile("\\b(elimina|eliminar|borra|borrar|quita|quitar|remove|delete)\\b").matcher(text).find();
      if(!removalCue||!mentions(userText,previous.name()))throw fail("La propuesta elimina un parámetro no solicitado: "+previous.name());
     }
    }
   }
   for(var p:edit.parameters()){
    boolean unchanged=old!=null&&old.parameters().stream().anyMatch(previous->previous.equals(p));
    if(!unchanged){if(!mentions(userText,p.name()))throw fail("El parámetro "+p.name()+" no fue solicitado.");typeInRequest(userText,p.type());}
   }
  }

 }
 private static void typeInRequest(String request,String type){
  if(type==null||type.isBlank())throw fail("Falta el tipo del método o parámetro.");
  String[] aliases=switch(type.toUpperCase(Locale.ROOT)){case "VOID"->new String[]{"void","sin retorno","no devuelve"};case "STRING"->new String[]{"string","cadena","texto"};case "BOOLEAN"->new String[]{"boolean","booleano","logico","bool"};case "INTEGER","INT"->new String[]{"integer","int","entero"};case "DECIMAL"->new String[]{"decimal"};case "DATE"->new String[]{"date","fecha"};default->new String[]{type};};
  if(Arrays.stream(aliases).noneMatch(a->mentions(request,a)))throw fail("El tipo "+type+" no aparece explícitamente en la solicitud.");
 }
 private static String text(JsonNode obj,String field,boolean required){var n=obj==null?null:obj.get(field);if(n==null||n.isNull()){if(required)throw fail("Falta "+field+".");return null;}if(!n.isString()||n.asString().isBlank())throw fail("Argumento inválido: "+field);return n.asString().trim();}
 private static boolean mentions(String text,String value){return text!=null&&value!=null&&Pattern.compile("(?<![a-z0-9_])"+Pattern.quote(normalize(value))+"(?![a-z0-9_])").matcher(normalize(text)).find();}
 private static String normalize(String value){return Normalizer.normalize(value,Normalizer.Form.NFD).replaceAll("\\p{M}+","").toLowerCase(Locale.ROOT);}
 private static AssistantPlanningException fail(String message){return new AssistantPlanningException(message);}
}
