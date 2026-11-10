package com.sinapuml.collaboration.protocol;

import java.util.UUID;

public record CollaborationActor(
        UUID id,
        String displayName
) {
}