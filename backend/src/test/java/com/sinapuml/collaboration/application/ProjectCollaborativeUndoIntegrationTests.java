package com.sinapuml.collaboration.application;

import com.sinapuml.auth.persistence.UserEntity;
import com.sinapuml.auth.persistence.UserRepository;
import com.sinapuml.collaboration.protocol.ProjectOperationApplied;
import com.sinapuml.collaboration.protocol.ProjectOperationRequest;
import com.sinapuml.collaboration.protocol.UmlCommandPayload;
import com.sinapuml.collaboration.protocol.UmlCommandType;
import com.sinapuml.project.application.ProjectService;
import com.sinapuml.project.domain.Project;
import com.sinapuml.project.domain.document.DiagramNodeLayout;
import com.sinapuml.project.domain.document.UmlClass;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest(properties = {
        "spring.mongodb.database=sinapuml_cu06_003_undo_test"
})
class ProjectCollaborativeUndoIntegrationTests {

    @Autowired
    private ProjectCollaborationService collaborationService;

    @Autowired
    private ProjectService projectService;

    @Autowired
    private UserRepository userRepository;

    @Test
    void deleteThenRestoreBehavesAsNewCollaborativeRevisions() {
        UUID ownerId = UUID.randomUUID();

        userRepository.save(
                new UserEntity(
                        ownerId,
                        "Undo Owner",
                        "cu06-003-"
                                + ownerId
                                + "@sinapuml.test",
                        "unused",
                        Instant.now()
                )
        );

        Project project =
                projectService.create(
                        ownerId,
                        "Undo colaborativo"
                );

        UUID classId =
                UUID.randomUUID();

        ProjectOperationApplied created =
                collaborationService.apply(
                        ownerId,
                        project.id(),
                        operation(
                                project.id(),
                                0L,
                                new UmlCommandPayload(
                                        UUID.randomUUID(),
                                        Instant.now(),
                                        UmlCommandType.CREATE_CLASS,
                                        null,
                                        null,
                                        new UmlClass(
                                                classId,
                                                "Animal",
                                                List.of()
                                        ),
                                        new DiagramNodeLayout(
                                                80,
                                                80,
                                                260,
                                                160
                                        ),
                                        null,
                                        null,
                                        null,
                                        null
                                )
                        )
                );

        assertEquals(
                1L,
                created.revision()
        );

        ProjectOperationApplied deleted =
                collaborationService.apply(
                        ownerId,
                        project.id(),
                        operation(
                                project.id(),
                                1L,
                                new UmlCommandPayload(
                                        UUID.randomUUID(),
                                        Instant.now(),
                                        UmlCommandType.DELETE_CLASS,
                                        classId,
                                        null,
                                        null,
                                        null,
                                        null,
                                        null,
                                        null,
                                        null
                                )
                        )
                );

        assertEquals(
                2L,
                deleted.revision()
        );

        ProjectOperationApplied restored =
                collaborationService.apply(
                        ownerId,
                        project.id(),
                        operation(
                                project.id(),
                                2L,
                                new UmlCommandPayload(
                                        UUID.randomUUID(),
                                        Instant.now(),
                                        UmlCommandType.RESTORE_CLASS,
                                        null,
                                        null,
                                        new UmlClass(
                                                classId,
                                                "Animal",
                                                List.of()
                                        ),
                                        new DiagramNodeLayout(
                                                80,
                                                80,
                                                260,
                                                160
                                        ),
                                        null,
                                        null,
                                        null,
                                        null,
                                        List.of()
                                )
                        )
                );

        assertEquals(
                3L,
                restored.revision()
        );

        Project reloaded =
                projectService.get(
                        ownerId,
                        project.id()
                );

        assertEquals(
                3L,
                reloaded.revision()
        );

        assertTrue(
                reloaded.document()
                        .umlModel()
                        .classes()
                        .stream()
                        .anyMatch(
                                umlClass ->
                                        umlClass.id()
                                                .equals(classId)
                        )
        );
    }

    private ProjectOperationRequest operation(
            UUID projectId,
            long revision,
            UmlCommandPayload command
    ) {
        return new ProjectOperationRequest(
                UUID.randomUUID(),
                projectId,
                UUID.randomUUID(),
                revision,
                command
        );
    }
}