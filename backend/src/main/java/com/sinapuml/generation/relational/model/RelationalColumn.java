package com.sinapuml.generation.relational.model;

import java.util.UUID;

public record RelationalColumn(RelationalColumnOrigin origin, UUID sourceElementId, String logicalName,
                               String name, RelationalDataType dataType, boolean nullable) { }
