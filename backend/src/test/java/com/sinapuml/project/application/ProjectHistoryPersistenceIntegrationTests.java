package com.sinapuml.project.application;

import com.sinapuml.project.domain.Project;
import com.sinapuml.project.domain.document.DiagramLayout;
import com.sinapuml.project.domain.document.ProjectDocument;
import com.sinapuml.project.domain.document.UmlClass;
import com.sinapuml.project.domain.document.UmlModel;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest(properties = {
        "spring.mongodb.database=sinapuml_history_persistence_test"
})
class ProjectHistoryPersistenceIntegrationTests {

    @Autowired
    private ProjectService projectService;

    @Test
    void restoredHistoricalDocumentCanBeSavedAsANewRevision() {
        UUID ownerId = UUID.randomUUID();

        Project project =
                projectService.create(
                        ownerId,
                        "Historial"
                );

        UUID animalId = UUID.randomUUID();

        ProjectDocument withAnimal =
                new ProjectDocument(
                        "1.0",
                        new UmlModel(
                                List.of(
                                        new UmlClass(
                                                animalId,
                                                "Animal",
                                                List.of()
                                        )
                                ),
                                List.of()
                        ),
                        DiagramLayout.empty()
                );

        Project revisionOne =
                projectService.saveDocument(
                        ownerId,
                        project.id(),
                        0L,
                        withAnimal
                );

        assertEquals(
                1L,
                revisionOne.revision()
        );

        Project revisionTwo =
                projectService.saveDocument(
                        ownerId,
                        project.id(),
                        1L,
                        ProjectDocument.empty()
                );

        assertEquals(
                2L,
                revisionTwo.revision()
        );

        Project revisionThree =
                projectService.saveDocument(
                        ownerId,
                        project.id(),
                        2L,
                        withAnimal
                );

        assertEquals(
                3L,
                revisionThree.revision()
        );

        assertEquals(
                1,
                revisionThree.document()
                        .umlModel()
                        .classes()
                        .size()
        );

        assertTrue(
                revisionThree.document()
                        .umlModel()
                        .classes()
                        .stream()
                        .anyMatch(
                                umlClass ->
                                        umlClass.id()
                                                .equals(animalId)
                        )
        );
    }
}