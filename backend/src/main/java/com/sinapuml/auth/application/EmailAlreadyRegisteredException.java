package com.sinapuml.auth.application;

public class EmailAlreadyRegisteredException extends RuntimeException {
    public EmailAlreadyRegisteredException() {
        super("An account with that email already exists");
    }
}