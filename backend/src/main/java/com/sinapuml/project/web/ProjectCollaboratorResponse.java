package com.sinapuml.project.web;

import com.sinapuml.project.access.ProjectAccessRole;
import com.sinapuml.project.application.ProjectCollaboratorView;

import java.time.Instant;
import java.util.UUID;

public record ProjectCollaboratorResponse(
        UUID userId,
        String displayName,
        String email,
        ProjectAccessRole accessRole,
        Instant joinedAt
) {
    public static ProjectCollaboratorResponse from(ProjectCollaboratorView view) {
        return new ProjectCollaboratorResponse(
                view.userId(),
                view.displayName(),
                view.email(),
                view.accessRole(),
                view.joinedAt()
        );
    }
}
