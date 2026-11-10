package com.sinapuml.demo;

import java.util.UUID;

public final class DemoScenario {

    public static final UUID OWNER_ID = UUID.fromString("27000000-0000-0000-0000-000000000001");
    public static final UUID EDITOR_ID = UUID.fromString("27000000-0000-0000-0000-000000000002");
    public static final UUID PROJECT_ID = UUID.fromString("27000000-0000-0000-0000-000000000100");
    public static final UUID MEMBERSHIP_ID = UUID.fromString("27000000-0000-0000-0000-000000000200");

    public static final String PROJECT_NAME = "Veterinaria CU-27";
    public static final String OWNER_EMAIL = "demo@sinapuml.local";
    public static final String EDITOR_EMAIL = "colaborador@sinapuml.local";
    public static final String PASSWORD = "sinapuml-demo";
    public static final String XMI_RESOURCE = "/demo/veterinaria-cu27.xmi";

    private DemoScenario() {
    }
}
