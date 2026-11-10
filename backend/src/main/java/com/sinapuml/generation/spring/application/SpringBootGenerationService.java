package com.sinapuml.generation.spring.application;

import com.sinapuml.generation.relational.RelationalMappingException;
import com.sinapuml.generation.relational.RelationalModelMapper;
import com.sinapuml.generation.spring.archive.DeterministicZipWriter;
import com.sinapuml.generation.spring.archive.SpringBootGenerationArtifact;
import com.sinapuml.generation.spring.model.SpringGenerationConfig;
import com.sinapuml.generation.spring.planning.SpringGenerationPlanner;
import com.sinapuml.generation.spring.rendering.SpringProjectRenderer;
import com.sinapuml.project.application.ProjectNotFoundException;
import com.sinapuml.project.application.ProjectRevisionConflictException;
import com.sinapuml.project.domain.Project;
import com.sinapuml.project.domain.document.UmlModel;
import com.sinapuml.project.persistence.ProjectMapper;
import com.sinapuml.project.persistence.ProjectRepository;
import java.util.List;
import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class SpringBootGenerationService {
    private final ProjectRepository projects;
    private final ProjectMapper mapper;
    private final RelationalModelMapper relationalMapper;
    private final SpringGenerationPlanner planner;
    private final SpringProjectRenderer renderer;
    private final DeterministicZipWriter archive;

    public SpringBootGenerationService(
            ProjectRepository projects,
            ProjectMapper mapper,
            RelationalModelMapper relationalMapper,
            SpringGenerationPlanner planner,
            SpringProjectRenderer renderer,
            DeterministicZipWriter archive
    ) {
        this.projects = projects;
        this.mapper = mapper;
        this.relationalMapper = relationalMapper;
        this.planner = planner;
        this.renderer = renderer;
        this.archive = archive;
    }

    @Transactional(readOnly = true)
    public SpringBootGenerationArtifact generate(
            UUID projectId,
            long baseRevision,
            SpringGenerationConfig config
    ) {
        return generate(projectId, baseRevision, config, SpringBootGenerationOptions.strict());
    }

    @Transactional(readOnly = true)
    public SpringBootGenerationArtifact generate(
            UUID projectId,
            long baseRevision,
            SpringGenerationConfig config,
            SpringBootGenerationOptions options
    ) {
        Project project = projects.findById(projectId)
                .map(mapper::toDomain)
                .orElseThrow(() -> new ProjectNotFoundException(projectId));
        if (project.revision() != baseRevision) {
            throw new ProjectRevisionConflictException(baseRevision, project.revision());
        }

        UmlModel canonicalModel = project.document().umlModel();
        UmlModel generationModel = options.useFirstAttributeAsIdentifier()
                ? SpringBootGenerationUmlPreparation.applyFirstAttributeIdentifiers(canonicalModel)
                : canonicalModel;

        try {
            var springModel = planner.plan(
                    relationalMapper.map(generationModel),
                    config
            );
            var rendered = renderer.render(springModel, options);
            if(canonicalModel.classes().stream().anyMatch(c -> !c.operations().isEmpty())) {
                var files = new java.util.ArrayList<>(rendered.files());
                files.add(new com.sinapuml.generation.spring.generated.GeneratedFile("uml-design.json", com.sinapuml.generation.spring.generated.GeneratedFileType.TEXT,
                        tools.jackson.databind.json.JsonMapper.builder().build().writeValueAsBytes(project.document())));
                files.add(new com.sinapuml.generation.spring.generated.GeneratedFile("UML-METHODS.md", com.sinapuml.generation.spring.generated.GeneratedFileType.TEXT,
                        "El diseño UML, incluidos métodos y parámetros, se conserva en uml-design.json. El generador crea CRUD y persistencia; no inventa cuerpos de lógica de negocio ni endpoints a partir de las firmas de métodos. Implemente esa lógica explícitamente antes de usarla.\n".getBytes(java.nio.charset.StandardCharsets.UTF_8)));
                rendered = new com.sinapuml.generation.spring.generated.GeneratedProject(rendered.artifactName(), files);
            }
            byte[] bytes = archive.write(rendered);
            return new SpringBootGenerationArtifact(
                    config.artifactName() + "-backend.zip",
                    "application/zip",
                    project.revision(),
                    bytes
            );
        } catch (RelationalMappingException exception) {
            if (!options.useFirstAttributeAsIdentifier()) {
                List<SpringBootGenerationPrimaryKeyFallback> candidates =
                        SpringBootGenerationUmlPreparation.fallbackCandidates(
                                canonicalModel,
                                exception.diagnostics()
                        );
                if (!candidates.isEmpty()) {
                    throw new SpringBootGenerationReadinessException(
                            exception.diagnostics(),
                            candidates
                    );
                }
            }
            throw exception;
        }
    }
}
