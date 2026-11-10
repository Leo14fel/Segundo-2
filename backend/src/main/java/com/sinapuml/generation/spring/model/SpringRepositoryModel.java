package com.sinapuml.generation.spring.model;

public record SpringRepositoryModel(String interfaceName, String entityClassName, String idTypeSimpleName,
                                    String idTypeQualifiedName, boolean generatedIdType) { }
