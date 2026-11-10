package com.sinapuml.projectassistant;

import com.sinapuml.project.domain.document.ProjectDocument;
import java.util.List;
import java.util.UUID;

public record ProjectAssistantContext(UUID projectId, String projectName, long currentRevision,
        ProjectDocument document, List<Member> members, List<ProjectAiMessage> recentMessages, List<ActivityFact> recentActivity, long totalRecordedActivities) {
    public ProjectAssistantContext {
        members = List.copyOf(members);
        recentMessages = List.copyOf(recentMessages);
        recentActivity = List.copyOf(recentActivity);
    }
    public ProjectAssistantContext(UUID projectId, String projectName, long currentRevision, ProjectDocument document, List<Member> members, List<ProjectAiMessage> recentMessages) {
        this(projectId, projectName, currentRevision, document, members, recentMessages, List.of(), 0);
    }
    public record ActivityFact(UUID actorId, String actorName, long revisionBefore, long revisionAfter, String description, java.time.Instant occurredAt) {}
    public record Member(UUID userId, String displayName, String role) { }
}
