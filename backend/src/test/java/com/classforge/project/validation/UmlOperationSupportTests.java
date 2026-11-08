package com.classforge.project.validation;
import com.classforge.project.domain.document.*;
import com.classforge.integration.xmi.*;
import com.classforge.collaboration.application.ProjectCommandExecutor;
import com.classforge.collaboration.protocol.*;
import org.junit.jupiter.api.Test;
import tools.jackson.databind.json.JsonMapper;
import java.util.*;
import java.time.Instant;
import static org.junit.jupiter.api.Assertions.*;
class UmlOperationSupportTests {
 private final UUID classId=UUID.randomUUID(),opId=UUID.randomUUID();
 private UmlOperation method(){return new UmlOperation(opId,"buscar",UmlVisibility.PUBLIC,"Libro",List.of(new UmlParameter(UUID.randomUUID(),"codigo","String")));}
 private ProjectDocument document(List<UmlOperation> methods){return new ProjectDocument("1.0",new UmlModel(List.of(new UmlClass(classId,"Libro",List.of(),methods)),List.of()),DiagramLayout.empty());}
 @Test void legacyJsonWithoutOperationsRemainsReadable(){var c=JsonMapper.builder().build().readValue("{\"id\":\""+classId+"\",\"name\":\"Libro\",\"attributes\":[]}",UmlClass.class);assertTrue(c.operations().isEmpty());}
 @Test void keepsMethodsThroughJsonAndXmiRoundTrip(){var original=document(List.of(method()));var mapper=JsonMapper.builder().build();assertEquals(original,mapper.readValue(mapper.writeValueAsString(original),ProjectDocument.class));var xml=new EnterpriseArchitectXmiExporter().export(UUID.randomUUID(),"Modelo",original);var imported=new EnterpriseArchitectXmiImporter().importXmi(xml).document();assertEquals(original.umlModel(),imported.umlModel());}
 @Test void validatesOverloadsAndRejectsDuplicatedSignatures(){var one=method();var two=new UmlOperation(UUID.randomUUID(),one.name(),one.visibility(),"Boolean",one.parameters().stream().map(p->new UmlParameter(UUID.randomUUID(),p.name(),p.type())).toList());var report=new ProjectDocumentValidator().analyze(document(List.of(one,two)));assertTrue(report.diagnostics().stream().anyMatch(d->d.code().equals("DUPLICATE_OPERATION_SIGNATURE")));}
 @Test void rejectsMissingIdsInvalidNamesAndVoidParameters(){var bad=new UmlOperation(null,"mal nombre",null,"Libro",List.of(new UmlParameter(null,"p","void")));var report=new ProjectDocumentValidator().analyze(document(List.of(bad)));assertFalse(report.valid());assertTrue(report.diagnostics().stream().anyMatch(d->d.code().equals("OPERATION_TYPE_INVALID")));}
 @Test void renamingClassDoesNotEraseMethods(){var original=document(List.of(method()));var command=new UmlCommandPayload(UUID.randomUUID(),Instant.now(),UmlCommandType.RENAME_CLASS,classId,"Publicacion",null,null,null,null,null,null);var result=new ProjectCommandExecutor().execute(original,command);assertEquals(original.umlModel().classes().getFirst().operations(),result.umlModel().classes().getFirst().operations());}
}
