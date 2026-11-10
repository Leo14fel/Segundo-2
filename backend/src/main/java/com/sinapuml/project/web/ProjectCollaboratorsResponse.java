package com.sinapuml.project.web;

import com.sinapuml.project.access.ProjectAccessRole;
import com.sinapuml.project.application.ProjectCollaboratorsView;

import java.util.List;

public record ProjectCollaboratorsResponse(
        ProjectAccessRole viewerRole,
        ProjectCollaboratorResponse owner,
        List<ProjectCollaboratorResponse> editors,
        List<ProjectInvitationResponse> pendingInvitations
) {
    public static ProjectCollaboratorsResponse from(ProjectCollaboratorsView view) {
        return new ProjectCollaboratorsResponse(
                view.viewerRole(),
                ProjectCollaboratorResponse.from(view.owner()),
                view.editors().stream()
                        .map(ProjectCollaboratorResponse::from)
                        .toList(),
                view.pendingInvitations().stream()
                        .map(ProjectInvitationResponse::from)
                        .toList()
        );
    }
}
