package com.sinapuml.auth.web;

import com.sinapuml.auth.persistence.UserEntity;

import java.util.UUID;

public record UserResponse(UUID id, String displayName, String email) {

    public static UserResponse from(UserEntity user) {
        return new UserResponse(user.getId(), user.getDisplayName(), user.getEmail());
    }
}