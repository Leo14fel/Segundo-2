package com.sinapuml.project.application;

import com.sinapuml.project.access.ProjectAccessRole;
import com.sinapuml.project.domain.Project;

import java.util.Objects;

public record AccessibleProject(
        Project project,
        ProjectAccessRole accessRole
) {
    public AccessibleProject {
        Objects.requireNonNull(project, "project is required");
        Objects.requireNonNull(accessRole, "accessRole is required");

        if (!accessRole.canRead()) {
            throw new IllegalArgumentException(
                    "Accessible project cannot use NONE role"
            );
        }
    }
}
