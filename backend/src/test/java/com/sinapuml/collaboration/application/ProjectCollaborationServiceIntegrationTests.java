package com.sinapuml.collaboration.application;

import com.sinapuml.auth.persistence.UserEntity;
import com.sinapuml.auth.persistence.UserRepository;
import com.sinapuml.collaboration.protocol.ProjectOperationApplied;
import com.sinapuml.collaboration.protocol.ProjectOperationRequest;
import com.sinapuml.collaboration.protocol.UmlCommandPayload;
import com.sinapuml.collaboration.protocol.UmlCommandType;
import com.sinapuml.project.application.ProjectNotFoundException;
import com.sinapuml.project.application.ProjectService;
import com.sinapuml.project.domain.Project;
import com.sinapuml.project.domain.document.DiagramNodeLayout;
import com.sinapuml.project.domain.document.UmlClass;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

@SpringBootTest(properties = {
        "spring.mongodb.database=sinapuml_cu06_service_test"
})
class ProjectCollaborationServiceIntegrationTests {

    @Autowired
    private ProjectCollaborationService collaborationService;

    @Autowired
    private ProjectService projectService;

    @Autowired
    private UserRepository userRepository;

    private UUID ownerId;
    private Project project;

    @BeforeEach
    void setUp() {
        ownerId = UUID.randomUUID();

        userRepository.save(
                new UserEntity(
                        ownerId,
                        "CU06 Owner",
                        "cu06-owner-"
                                + ownerId
                                + "@sinapuml.test",
                        "unused",
                        Instant.now()
                )
        );

        project =
                projectService.create(
                        ownerId,
                        "Veterinaria"
                );
    }

    @Test
    void acceptedOperationPersistsAndIncrementsExactlyOneRevision() {
        UUID classId = UUID.randomUUID();

        ProjectOperationApplied applied =
                collaborationService.apply(
                        ownerId,
                        project.id(),
                        createClassOperation(
                                project.id(),
                                0L,
                                classId,
                                "Animal"
                        )
                );

        assertEquals(
                1L,
                applied.revision()
        );

        Project reloaded =
                projectService.get(
                        ownerId,
                        project.id()
                );

        assertEquals(
                1L,
                reloaded.revision()
        );

        assertEquals(
                classId,
                reloaded.document()
                        .umlModel()
                        .classes()
                        .getFirst()
                        .id()
        );
    }

    @Test
    void staleOperationIsRejectedWithoutChangingState() {
        collaborationService.apply(
                ownerId,
                project.id(),
                createClassOperation(
                        project.id(),
                        0L,
                        UUID.randomUUID(),
                        "Animal"
                )
        );

        ProjectOperationRejectedException exception =
                assertThrows(
                        ProjectOperationRejectedException.class,
                        () ->
                                collaborationService.apply(
                                        ownerId,
                                        project.id(),
                                        createClassOperation(
                                                project.id(),
                                                0L,
                                                UUID.randomUUID(),
                                                "Cita"
                                        )
                                )
                );

        assertEquals(
                "REVISION_CONFLICT",
                exception.getCode()
        );

        assertEquals(
                1L,
                exception.getCurrentRevision()
        );

        Project reloaded =
                projectService.get(
                        ownerId,
                        project.id()
                );

        assertEquals(
                1L,
                reloaded.revision()
        );

        assertEquals(
                1,
                reloaded.document()
                        .umlModel()
                        .classes()
                        .size()
        );
    }

    @Test
    void invalidCommandIsRejectedAndNotPersisted() {
        collaborationService.apply(
                ownerId,
                project.id(),
                createClassOperation(
                        project.id(),
                        0L,
                        UUID.randomUUID(),
                        "Animal"
                )
        );

        ProjectOperationRejectedException exception =
                assertThrows(
                        ProjectOperationRejectedException.class,
                        () ->
                                collaborationService.apply(
                                        ownerId,
                                        project.id(),
                                        createClassOperation(
                                                project.id(),
                                                1L,
                                                UUID.randomUUID(),
                                                "Animal"
                                        )
                                )
                );

        assertEquals(
                "DUPLICATE_CLASS_NAME",
                exception.getCode()
        );

        Project reloaded =
                projectService.get(
                        ownerId,
                        project.id()
                );

        assertEquals(
                1L,
                reloaded.revision()
        );

        assertEquals(
                1,
                reloaded.document()
                        .umlModel()
                        .classes()
                        .size()
        );
    }

    @Test
    void ownerCheckIsAlsoEnforcedInsideTransactionalService() {
        UUID strangerId = UUID.randomUUID();

        userRepository.save(
                new UserEntity(
                        strangerId,
                        "Stranger",
                        "cu06-stranger-"
                                + strangerId
                                + "@sinapuml.test",
                        "unused",
                        Instant.now()
                )
        );

        assertThrows(
                ProjectNotFoundException.class,
                () ->
                        collaborationService.apply(
                                strangerId,
                                project.id(),
                                createClassOperation(
                                        project.id(),
                                        0L,
                                        UUID.randomUUID(),
                                        "Intrusa"
                                )
                        )
        );
    }

    private ProjectOperationRequest createClassOperation(
            UUID projectId,
            long baseRevision,
            UUID classId,
            String name
    ) {
        return new ProjectOperationRequest(
                UUID.randomUUID(),
                projectId,
                UUID.randomUUID(),
                baseRevision,
                new UmlCommandPayload(
                        UUID.randomUUID(),
                        Instant.now(),
                        UmlCommandType.CREATE_CLASS,
                        null,
                        null,
                        new UmlClass(
                                classId,
                                name,
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
        );
    }
}