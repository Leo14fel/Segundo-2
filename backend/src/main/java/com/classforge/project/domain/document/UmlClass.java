package com.classforge.project.domain.document;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.UUID;

public record UmlClass(
        UUID id,
        String name,
        List<UmlAttribute> attributes,
        List<UmlOperation> operations
) {
    public UmlClass(UUID id, String name, List<UmlAttribute> attributes) { this(id, name, attributes, List.of()); }

    public UmlClass {
        operations = operations == null ? List.of() : Collections.unmodifiableList(new ArrayList<>(operations));
        attributes = attributes == null
                ? List.of()
                : Collections.unmodifiableList(new ArrayList<>(attributes));
    }
}