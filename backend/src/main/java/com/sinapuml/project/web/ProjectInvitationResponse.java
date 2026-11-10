package com.sinapuml.project.web;

import com.sinapuml.project.application.ProjectInvitationView;
import com.sinapuml.project.persistence.ProjectInvitationStatus;

import java.time.Instant;
import java.util.UUID;

public record ProjectInvitationResponse(
        UUID id,
        UUID projectId,
        String projectName,
        String invitedEmail,
        UUID invitedByUserId,
        String invitedByDisplayName,
        ProjectInvitationStatus status,
        Instant createdAt,
        Instant respondedAt
) {
    public static ProjectInvitationResponse from(ProjectInvitationView view) {
        return new ProjectInvitationResponse(
                view.id(),
                view.projectId(),
                view.projectName(),
                view.invitedEmail(),
                view.invitedByUserId(),
                view.invitedByDisplayName(),
                view.status(),
                view.createdAt(),
                view.respondedAt()
        );
    }
}
