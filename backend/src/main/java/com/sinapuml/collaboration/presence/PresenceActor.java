package com.sinapuml.collaboration.presence;

import java.util.UUID;

public record PresenceActor(
        UUID id,
        String displayName
) {
}