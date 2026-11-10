package com.sinapuml.generation.spring.model;

import com.sinapuml.project.domain.document.UmlRelationshipType;
import java.util.List;
import java.util.UUID;

public record SpringManyToManyRelationModel(UUID sourceRelationshipId, UmlRelationshipType umlType,
                                            String fieldName, String targetEntityClassName,
                                            String joinTableName, List<SpringJoinColumnModel> joinColumns,
                                            List<SpringJoinColumnModel> inverseJoinColumns) {
    public SpringManyToManyRelationModel {
        joinColumns = List.copyOf(joinColumns == null ? List.of() : joinColumns);
        inverseJoinColumns = List.copyOf(inverseJoinColumns == null ? List.of() : inverseJoinColumns);
    }
}
