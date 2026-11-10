package com.sinapuml.assistant;

import com.sinapuml.assistant.tools.AssistantNativeToolPlanner;
import com.sinapuml.collaboration.protocol.UmlCommandPayload;
import com.sinapuml.project.application.ProjectNotFoundException;
import com.sinapuml.project.application.ProjectService;
import com.sinapuml.project.domain.Project;
import com.sinapuml.project.domain.document.ProjectDocument;
import com.sinapuml.project.persistence.ProjectMembershipEntity;
import com.sinapuml.project.persistence.ProjectMembershipRepository;
import com.sinapuml.project.validation.ProjectDocumentValidator;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.mock.web.MockMultipartFile;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.clearInvocations;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;

@SpringBootTest(properties = {
        "spring.mongodb.database=sinapuml_cu31_assistant_access_test"
})
class AssistantMembershipAccessIntegrationTests {

    @Autowired
    private ProjectService projectService;

    @Autowired
    private ProjectMembershipRepository projectMembershipRepository;

    @Test
    void editorCanPlanTextButNoneIsRejectedBeforeCallingTheLlm() {
        UUID ownerId = UUID.randomUUID();
        UUID editorId = UUID.randomUUID();
        UUID noneId = UUID.randomUUID();

        Project project = projectService.create(ownerId, "Assistant CU31");
        projectMembershipRepository.save(
                ProjectMembershipEntity.editor(project.id(), editorId)
        );

        AssistantNativeToolPlanner gateway = mock(AssistantNativeToolPlanner.class);
        UmlAssistantCommandResolver resolver = mock(UmlAssistantCommandResolver.class);
        ProjectDocumentValidator validator = mock(ProjectDocumentValidator.class);

        AssistantSemanticPlan plan =
                new AssistantSemanticPlan("Sin cambios", List.of());
        UmlCommandPayload batch =
                UmlCommandPayload.batch("Sin cambios", List.of());

        when(gateway.plan(anyString(), any(ProjectDocument.class))).thenReturn(plan);
        when(resolver.resolve(any(AssistantSemanticPlan.class), any(ProjectDocument.class))).thenReturn(batch);
        when(resolver.preview(any(ProjectDocument.class), any(UmlCommandPayload.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));

        AssistantPlanService service =
                new AssistantPlanService(
                        projectService,
                        gateway,
                        resolver,
                        validator
                );

        AssistantPlanResponse response =
                service.plan(editorId, project.id(), "No cambies nada");

        assertEquals(0L, response.baseRevision());
        assertEquals("TEXT", response.source());

        clearInvocations(gateway);

        assertThrows(
                ProjectNotFoundException.class,
                () -> service.plan(noneId, project.id(), "No cambies nada")
        );

        verifyNoInteractions(gateway);
    }

    @Test
    void editorCanReachVoicePipelineButNoneIsRejectedBeforeStt() {
        UUID ownerId = UUID.randomUUID();
        UUID editorId = UUID.randomUUID();
        UUID noneId = UUID.randomUUID();

        Project project = projectService.create(ownerId, "Voice CU31");
        projectMembershipRepository.save(
                ProjectMembershipEntity.editor(project.id(), editorId)
        );

        SpeechToTextGateway speechToTextGateway = mock(SpeechToTextGateway.class);
        AssistantPlanService planService = mock(AssistantPlanService.class);
        AssistantVoiceService voiceService =
                new AssistantVoiceService(
                        projectService,
                        speechToTextGateway,
                        planService
                );

        MockMultipartFile audio =
                new MockMultipartFile(
                        "audio",
                        "cu31.wav",
                        "audio/wav",
                        new byte[] {1, 2, 3, 4}
                );

        AssistantPlanResponse expected =
                new AssistantPlanResponse(
                        "VOICE",
                        "crea animal",
                        0L,
                        "Crear Animal",
                        new AssistantSemanticPlan("Crear Animal", List.of()),
                        UmlCommandPayload.batch("Crear Animal", List.of())
                );

        when(speechToTextGateway.transcribe(any(byte[].class), anyString()))
                .thenReturn("crea animal");
        when(planService.planVoice(editorId, project.id(), "crea animal"))
                .thenReturn(expected);

        AssistantPlanResponse actual =
                voiceService.plan(editorId, project.id(), audio);

        assertEquals(expected, actual);

        clearInvocations(speechToTextGateway);

        assertThrows(
                ProjectNotFoundException.class,
                () -> voiceService.plan(noneId, project.id(), audio)
        );

        verifyNoInteractions(speechToTextGateway);
    }
}
