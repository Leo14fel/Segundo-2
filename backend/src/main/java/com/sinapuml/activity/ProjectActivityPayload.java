package com.sinapuml.activity;

import com.sinapuml.collaboration.protocol.UmlCommandPayload;
import com.sinapuml.project.domain.document.ProjectDocument;
import java.util.List;

/** Versioned audit envelope retains the accepted command and both authoritative snapshots. */
public record ProjectActivityPayload(int version, UmlCommandPayload command,
        ProjectDocument beforeDocument, ProjectDocument afterDocument, List<ActivityChange> changes) { }
