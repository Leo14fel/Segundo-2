package com.sinapuml.assistant.tools;

import com.sinapuml.assistant.*;
import com.sinapuml.collaboration.application.ProjectCommandExecutor;
import com.sinapuml.collaboration.protocol.*;
import com.sinapuml.project.domain.document.*;
import org.junit.jupiter.api.Test;
import tools.jackson.databind.json.JsonMapper;
import java.util.*;
import java.time.Instant;
import static org.junit.jupiter.api.Assertions.*;

class AssistantOperationToolTests {
 private final JsonMapper json=JsonMapper.builder().build();
 private final AssistantEntityReferenceResolver entity=new AssistantEntityReferenceResolver();
 private final AssistantIntentHintResolver hints=new AssistantIntentHintResolver();
 private final DynamicUmlToolCatalog catalogs=new DynamicUmlToolCatalog(hints);
 private final UmlToolCallResolver tools=new UmlToolCallResolver(entity,new AssistantLiteralArgumentBinder());
 private final ProjectCommandExecutor executor=new ProjectCommandExecutor();
 private final UmlAssistantCommandResolver commands=new UmlAssistantCommandResolver(executor,new AssistantPlanNormalizer());
 private final UUID classId=UUID.randomUUID();
 private UmlOperation operation(String type){return new UmlOperation(UUID.randomUUID(),"buscar",UmlVisibility.PRIVATE,"Libro",List.of(new UmlParameter(UUID.randomUUID(),"codigo",type)));}
 private ProjectDocument doc(UmlOperation...ops){return new ProjectDocument("1.0",new UmlModel(List.of(new UmlClass(classId,"Libro",List.of(new UmlAttribute(UUID.randomUUID(),"id",UmlDataType.UUID,null,UmlVisibility.PRIVATE,false,true)),List.of(ops))),List.of()),DiagramLayout.empty());}
 private AssistantSemanticPlan resolve(String text,ProjectDocument doc,String args){var call=new AssistantToolInvocation("method-call",AssistantToolName.EDIT_OPERATION,json.readTree(args));return tools.resolve(text,List.of(call),catalogs.buildForTools(doc,List.of(AssistantToolName.EDIT_OPERATION)),doc).plan();}
 @Test void nativeRoutingCreatesMethodWithoutModifyingOriginalUntilCommandIsExecuted(){
  var before=doc();
  AssistantToolCallingGateway gateway=(text,document,catalog,history)->catalog.definitions().getFirst().name()==AssistantToolName.ROUTE_REQUEST
    ?List.of(new AssistantToolInvocation("route",AssistantToolName.ROUTE_REQUEST,json.readTree("{\"steps\":[\"create_class\"]}")))
    :List.of(new AssistantToolInvocation("create",AssistantToolName.EDIT_OPERATION,json.readTree("{\"existing_class\":\"Libro\",\"change\":\"CREATE\",\"name\":\"disponible\",\"return_type\":\"BOOLEAN\",\"parameters\":[{\"name\":\"fecha\",\"type\":\"DATE\"}]}")));
  var planner=new AssistantNativeToolPlanner(catalogs,gateway,tools,new AssistantToolRouteAdjudicator(hints,entity,new AssistantCompoundRequestDetector()),commands,new AssistantSemanticCompiler(entity),new AssistantPlanGroundingFilter(entity),new AssistantPlanNormalizer());
  var plan=planner.plan("Agrega el método disponible a Libro con retorno BOOLEAN y parámetro fecha DATE",before);
  assertEquals(AssistantActionType.EDIT_OPERATION,plan.actions().getFirst().type());assertTrue(before.umlModel().classes().getFirst().operations().isEmpty());
  var batch=commands.resolve(plan,before);assertEquals(UmlCommandType.SET_CLASS_OPERATIONS,batch.safeCommands().getFirst().type());
  var after=commands.preview(before,batch);assertEquals("disponible",after.umlModel().classes().getFirst().operations().getFirst().name());assertEquals(before.umlModel().classes().getFirst().attributes(),after.umlModel().classes().getFirst().attributes());
 }
 @Test void updatePreservesOmittedParametersReturnVisibilityAndId(){var old=operation("STRING");var before=doc(old);String args=json.writeValueAsString(Map.of("existing_class","Libro","change","UPDATE","existing_operation_ref",AssistantOperationSupport.label(before.umlModel().classes().getFirst(),old),"name","consultar"));var plan=resolve("Renombra el método buscar de Libro a consultar",before,args);var after=commands.preview(before,commands.resolve(plan,before)).umlModel().classes().getFirst().operations().getFirst();assertEquals(old.id(),after.id());assertEquals(old.parameters(),after.parameters());assertEquals(old.visibility(),after.visibility());assertEquals(old.returnType(),after.returnType());assertEquals("consultar",after.name());}
 @Test void rejectsAmbiguousOverloadDeletion(){var one=operation("STRING");var before=doc(one,operation("UUID"));String args=json.writeValueAsString(Map.of("existing_class","Libro","change","DELETE","existing_operation_ref",AssistantOperationSupport.label(before.umlModel().classes().getFirst(),one)));assertThrows(AssistantPlanningException.class,()->resolve("Elimina el método buscar de Libro",before,args));assertEquals(2,before.umlModel().classes().getFirst().operations().size());}
 @Test void explicitOverloadDeletionKeepsSibling(){var one=operation("STRING");var two=operation("UUID");var before=doc(one,two);String args=json.writeValueAsString(Map.of("existing_class","Libro","change","DELETE","existing_operation_ref",AssistantOperationSupport.label(before.umlModel().classes().getFirst(),one)));var plan=resolve("Elimina el método buscar(STRING) de Libro",before,args);assertEquals(List.of(two),commands.preview(before,commands.resolve(plan,before)).umlModel().classes().getFirst().operations());}
 @Test void rejectsInventedIdentifiersTypesAndWrongMutation(){var before=doc();String create="{\"existing_class\":\"Libro\",\"change\":\"CREATE\",\"name\":\"inventado\",\"return_type\":\"STRING\"}";assertThrows(AssistantPlanningException.class,()->resolve("Agrega el método disponible a Libro sin retorno",before,create));assertThrows(AssistantPlanningException.class,()->resolve("Revisa el método inventado de Libro STRING",before,create));}
 @Test void cannotDeleteWholeMethodWhenUserAsksToDeleteParameter(){var old=operation("STRING");var before=doc(old);String args=json.writeValueAsString(Map.of("existing_class","Libro","change","DELETE","existing_operation_ref",AssistantOperationSupport.label(before.umlModel().classes().getFirst(),old)));assertThrows(AssistantPlanningException.class,()->resolve("Elimina el parámetro codigo del método buscar de Libro",before,args));}
 @Test void canonicalOperationCommandCannotRenameClassOrReplaceAttributes(){var before=doc();var payload=new UmlClass(classId,"NombreInventado",List.of(),List.of(operation("STRING")));var command=new UmlCommandPayload(UUID.randomUUID(),Instant.now(),UmlCommandType.SET_CLASS_OPERATIONS,classId,null,payload,null,null,null,null,null);var after=executor.execute(before,command);assertEquals("Libro",after.umlModel().classes().getFirst().name());assertEquals(before.umlModel().classes().getFirst().attributes(),after.umlModel().classes().getFirst().attributes());}
 @Test void rejectsDuplicateMethodSignatureWithoutPublishingPartialState(){var old=operation("STRING");var before=doc(old);var plan=resolve("Agrega el método buscar a Libro con parámetro codigo STRING y retorno Libro",before,"{\"existing_class\":\"Libro\",\"change\":\"CREATE\",\"name\":\"buscar\",\"return_type\":\"Libro\",\"parameters\":[{\"name\":\"codigo\",\"type\":\"STRING\"}]}");assertThrows(AssistantPlanningException.class,()->commands.resolve(plan,before));assertEquals(List.of(old),before.umlModel().classes().getFirst().operations());}
 @Test void rejectsMultipleChangesRatherThanApplyingOnlyOne(){assertThrows(AssistantPlanningException.class,()->AssistantOperationSupport.singleRequest("Agrega los métodos buscar y guardar de Libro"));assertThrows(AssistantPlanningException.class,()->AssistantOperationSupport.singleRequest("Agrega el método buscar a Libro y elimina la clase Venta"));}

 @Test void methodNamedClassOrAttributeDoesNotStealTheirExistingIntent(){assertNotEquals(AssistantActionType.EDIT_OPERATION,hints.resolve("Renombra la clase Metodo a Servicio",doc()).map(AssistantIntentHintResolver.IntentHint::actionType).orElse(null));assertNotEquals(AssistantActionType.EDIT_OPERATION,hints.resolve("Agrega el atributo metodo STRING a Libro",doc()).map(AssistantIntentHintResolver.IntentHint::actionType).orElse(null));}

 @Test void classNameInRequestDoesNotAuthorizeAnInventedReturnType(){var before=doc();assertThrows(AssistantPlanningException.class,()->resolve("Agrega el método disponible a Libro",before,"{\"existing_class\":\"Libro\",\"change\":\"CREATE\",\"name\":\"disponible\",\"return_type\":\"Libro\"}"));}

}
