package com.classforge.push;
public interface WebPushGateway { int send(PushSubscription subscription, byte[] payload) throws Exception; }
