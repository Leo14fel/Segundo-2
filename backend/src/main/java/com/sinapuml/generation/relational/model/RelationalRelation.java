package com.sinapuml.generation.relational.model;

import com.sinapuml.project.domain.document.UmlRelationshipType;
import java.util.UUID;

public record RelationalRelation(UUID sourceRelationshipId, UmlRelationshipType umlType,
                                 String sourceTableName, String targetTableName,
                                 RelationalCardinality sourceCardinality, RelationalCardinality targetCardinality,
                                 RelationalRelationStorage storage, String owningTableName,
                                 String joinTableName, RelationalReferentialAction onDelete) { }
