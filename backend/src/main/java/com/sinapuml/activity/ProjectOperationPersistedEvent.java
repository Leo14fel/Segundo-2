package com.sinapuml.activity;

import com.sinapuml.collaboration.protocol.UmlCommandPayload;
import com.sinapuml.project.domain.document.ProjectDocument;
import java.time.Instant;
import java.util.UUID;

/** Published synchronously inside the document transaction, after successful validation. */
public record ProjectOperationPersistedEvent(
        UUID projectId, UUID operationId, UUID actorUserId, String actorDisplayName,
        long revisionBefore, long revisionAfter, ActivitySource source,
        UmlCommandPayload command, ProjectDocument beforeDocument,
        ProjectDocument afterDocument, Instant occurredAt) { }
