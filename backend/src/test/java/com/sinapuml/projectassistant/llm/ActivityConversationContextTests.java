package com.sinapuml.projectassistant.llm;
import com.sinapuml.projectassistant.*;
import com.sinapuml.project.domain.document.ProjectDocument;
import org.junit.jupiter.api.Test;
import tools.jackson.databind.json.JsonMapper;
import java.util.*;
import java.time.Instant;
import static org.junit.jupiter.api.Assertions.*;
class ActivityConversationContextTests {
 @Test void includesBoundedActivityWithRealAuthorAndCoverageAsUntrustedData(){
  var author=UUID.randomUUID();
  var fact=new ProjectAssistantContext.ActivityFact(author,"Ana",2,3,"Agregó Cliente",Instant.parse("2026-11-08T12:00:00Z"));
  var context=new ProjectAssistantContext(UUID.randomUUID(),"Equipo",3,ProjectDocument.empty(),List.of(),List.of(),List.of(fact),80);
  var support=new ProjectAssistantConversationSupport(JsonMapper.builder().build(),120000);
  var turns=support.conversation(context,"Qué avanzó el equipo",AssistantMode.SUMMARY_CURRENT);
  assertTrue(turns.get(1).content().contains("Ana"));assertTrue(turns.get(1).content().contains(author.toString()));
  assertTrue(turns.get(1).content().contains("\"truncated\":true"));
  assertFalse(turns.get(0).content().contains(author.toString()));
 }
 @Test void rejectsExcessiveHistoricalContextRatherThanSilentlyCuttingIt(){
  var fact=new ProjectAssistantContext.ActivityFact(UUID.randomUUID(),"Ana",0,1,"x".repeat(20000),Instant.now());
  var context=new ProjectAssistantContext(UUID.randomUUID(),"Equipo",1,ProjectDocument.empty(),List.of(),List.of(),List.of(fact),1);
  var support=new ProjectAssistantConversationSupport(JsonMapper.builder().build(),10000);
  assertThrows(ProjectAssistantUnavailableException.class,()->support.conversation(context,"Resumen",AssistantMode.SUMMARY_CURRENT));
 }
}
