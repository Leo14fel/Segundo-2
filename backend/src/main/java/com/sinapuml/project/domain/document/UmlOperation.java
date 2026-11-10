package com.sinapuml.project.domain.document;
import java.util.*;
public record UmlOperation(UUID id, String name, UmlVisibility visibility, String returnType, List<UmlParameter> parameters) {
 public UmlOperation { returnType=returnType==null||returnType.isBlank()||returnType.equalsIgnoreCase("void")?null:returnType; parameters=parameters==null?List.of():Collections.unmodifiableList(new ArrayList<>(parameters)); }
}
