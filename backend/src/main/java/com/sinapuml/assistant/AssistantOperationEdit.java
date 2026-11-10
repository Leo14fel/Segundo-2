package com.sinapuml.assistant;
import com.sinapuml.project.domain.document.*;
import java.util.*;
/** IDs for new members are allocated by Java, never supplied by the model. */
public record AssistantOperationEdit(String change, UUID operationId, String name, String returnType, UmlVisibility visibility, List<UmlParameter> parameters) {
 public AssistantOperationEdit { parameters=parameters==null?null:List.copyOf(parameters); }
}
