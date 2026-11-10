package com.sinapuml.generation.spring.api;

import com.sinapuml.generation.spring.model.SpringEntityIdModel;

public record SpringApiManyRelationModel(
        String fieldName,
        String targetEntityClassName,
        String targetRepositoryName,
        SpringEntityIdModel targetId
) { }
