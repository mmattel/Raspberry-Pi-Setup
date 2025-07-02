# Mosquitto MQTT broker

   * [Overview](#overview)
   * [Installing Mosquitto with Docker](#installing-mosquitto-with-docker)
   * [Configuration](#configuration)
      * [Basic Configuration](#basic-configuration)
      * [Set a Password Authentication](#set-a-password-authentication)
      * [Reboot Persist Messages](#reboot-persist-messages)
   * [Accessing Mosquitto](#accessing-mosquitto)


<!-- Created by https://github.com/ekalinin/github-markdown-toc -->

## Overview

[Mosquitto](https://mosquitto.org) is an open source message broker that implements the MQTT protocol.

The MQTT protocol provides a lightweight method of carrying out messaging using a publish/subscribe model. This makes it suitable for Internet of Things messaging such as with low power sensors or mobile devices such as phones, embedded computers or microcontrollers.

<p align="center">
<img src="../images/MosquittoMQTTArchitecture.png" width="450" title=" Mosquitto MQTT broker">
</p>

The Mosquitto MQTT broker is the central hub for messages. The the [Z-Wave to MQTT Gateway](./zwavejs2mqtt.md) and [Home Assistant](./ha_install.md) will connect to it.

See the mosquitto broker as a hub for messages without knowledge of the sender and topic, which publishes (broadcasts) the messages recieved. To do so, it uses a port the publisher and subscriber connect to. It is on the  publisher/subscriber to decide about the topic sent or recieved. 

## Installing Mosquitto with Docker

Note that the container will fail starting up as a default config file is missing. To fix this, just copy the [mosquitto.conf](https://github.com/eclipse/mosquitto/blob/master/mosquitto.conf) file from github to the `docker/mosquitto/config` directory and restart the container.

```
version: "3"
services:
  mosquitto:
    container_name: mosquitto
    image: eclipse-mosquitto
    restart: always
    stdin_open: true     # comment if you do not need
    tty: true            # comment if you do not need
    ports:
      - "1883:1883"
    logging:
      driver: "json-file"
      options:
        max-size: "200k"
        max-file: "10"
    volumes:
      - "/home/<your-user>/docker/mosquitto/config:/mosquitto/config"
      - "/home/<your-user>/docker/mosquitto/data:/mosquitto/data"
      - "/home/<your-user>/docker/mosquitto/log:/mosquitto/log"
    environment:
      - TZ=Europe/Vienna
    user: "${LOCAL_USER}:${LOCAL_GROUP}"
```

## Configuration

To configure mosquitto, edit the `~/docker/mosquitto/config/mosquitto.conf` file. When done, restart the container.

### Basic Configuration

Because we are only working on the local LAN, you can set the `listerer` in section _Extra listeners_ to allow all IP and port 1883:

```
listener 1883 0.0.0.0
```
With low security and not recommended, the `allow_anonymous` setting in the _Security_ section config option can be set to `true`.
```
allow_anonymous true
```

### Set a Password Authentication

If you want to set a password for security reasons, which is highly recommended, proceed with the following, replace `<user-name>` accordingly:

- In portainer, go into the command shell of the mosquitto container using `bin/sh`
- Run `mosquitto_passwd -c /mosquitto/config/password.txt <user-name>`
- You will get asked for a user and a password - remember it.
- Use `mosquitto_passwd --help` to see all the arguments and options (like for updating the password)
- Exit the command shell with button `Disconnect`

Now change the `mosquitto.conf` file from your RPi to configure it for password authentication

```
allow_anonymous false
password_file /mosquitto/config/password.txt
```

### Reboot Persist Messages  

When the container or the RPi gets rebootet, the latest messages will not survive the reboot if not configured otherwise.
 
In the _Persistence_ section, set the following keys:

```
persistence true
persistence_file mosquitto.db
persistence_location /mosquitto/data/
```

This will create a file on the RPi `docker/mosquitto/data/mosquitto.db` which is only a few KB in size and updated on new messages.

## Accessing Mosquitto

To access mosquitto, it might be neccessary to use not only the hostname of the RPi but the FQDN - check it out.
