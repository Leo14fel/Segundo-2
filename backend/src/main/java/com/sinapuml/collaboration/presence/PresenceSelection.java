package com.sinapuml.collaboration.presence;

import java.util.UUID;

public record PresenceSelection(
        UUID elementId,
        PresenceElementType elementType
) {
}