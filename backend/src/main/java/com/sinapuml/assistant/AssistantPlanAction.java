package com.sinapuml.assistant;

import com.sinapuml.project.domain.document.UmlDataType;
import com.sinapuml.project.domain.document.UmlRelationshipType;
import com.sinapuml.project.domain.document.UmlVisibility;

import java.util.List;

public record AssistantPlanAction(
        AssistantActionType type,
        String className,
        String newName,
        List<AssistantAttributePlan> attributes,
        String attributeName,
        String newAttributeName,
        UmlDataType dataType,
        String customTypeName,
        UmlVisibility visibility,
        Boolean nullable,
        Boolean identifier,
        String sourceClassName,
        String targetClassName,
        UmlRelationshipType relationshipType,
        Integer sourceLower,
        Integer sourceUpper,
        Integer targetLower,
        Integer targetUpper,
        AssistantOperationEdit operationEdit
) {
    public AssistantPlanAction(
        AssistantActionType type,
        String className,
        String newName,
        List<AssistantAttributePlan> attributes,
        String attributeName,
        String newAttributeName,
        UmlDataType dataType,
        String customTypeName,
        UmlVisibility visibility,
        Boolean nullable,
        Boolean identifier,
        String sourceClassName,
        String targetClassName,
        UmlRelationshipType relationshipType,
        Integer sourceLower,
        Integer sourceUpper,
        Integer targetLower,
        Integer targetUpper
    ) { this(type, className, newName, attributes, attributeName, newAttributeName, dataType, customTypeName, visibility, nullable, identifier, sourceClassName, targetClassName, relationshipType, sourceLower, sourceUpper, targetLower, targetUpper, null); }
    public static AssistantPlanAction operation(String className, AssistantOperationEdit edit) {
        return new AssistantPlanAction(AssistantActionType.EDIT_OPERATION,className,null,List.of(),null,null,null,null,null,null,null,null,null,null,null,null,null,null,edit);
    }
    public List<AssistantAttributePlan> safeAttributes() {
        return attributes == null
                ? List.of()
                : List.copyOf(attributes);
    }
}