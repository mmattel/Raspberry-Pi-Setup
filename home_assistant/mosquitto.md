# Mosquitto MQTT broker

   * [Overview](#overview)
   * [Installing Mosquitto with Docker](#installing-mosquitto-with-docker)
   * [Set a Password authentication](#set-a-password-authentication)
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
    restart: unless-stopped
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
      - "/home/<your-user>l/docker/mosquitto/config:/mosquitto/config"
      - "/home/<your-user>/docker/mosquitto/data:/mosquitto/data"
      - "/home/<your-user>/docker/mosquitto/log:/mosquitto/log"
    environment:
      - TZ=Europe/Vienna
    user: "${LOCAL_USER}:${LOCAL_GROUP}"
```

Because we are only working on the local LAN, you can set the `listerer` in section _Extra listeners_ and the `allow_anonymous` in the _Security_ section config option to:

`vi docker/mosquitto/config/mosquitto.conf`

```
listener 1883 0.0.0.0
allow_anonymous true
```

## Set a Password authentication

If you want to set a password for security reasons, proceed with the following, replace `<user-name>` accordingly:

- In portainer, go into the command shell of the mosquitto container using `bin/sh`
- Run `mosquitto_passwd -c /mosquitto/config/password.txt <user-name>`
- You will get asked for a user and a password - remember it.
- Use `mosquitto_passwd --help` to see all the arguments and options (like for updating the password)
- Exit the command shell with button `Disconnect`

Now change the mosquitto.conf file from your RPi to configure it for password authentication

`vi docker/mosquitto/config/mosquitto.conf`

```
allow_anonymous false
password_file /mosquitto/config/password.txt
```

When done, restart the container.

## Accessing Mosquitto

To access mosquitto, it might be neccessary to use not only the hostname of the RPi but the FQDN - check it out.
