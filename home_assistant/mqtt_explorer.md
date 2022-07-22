# MQTT Explorer

The [MQTT Explorer](https://mqtt-explorer.com) is a nice graphical interface for reading messages of mosquitto. To use the MQTT Explorer as [container](https://hub.docker.com/r/smeagolworms4/mqtt-explorer) accessible via an web interface, we use [Smeagolworms4](https://github.com/Smeagolworms4/MQTT-Explorer) fork.

## Installing MQTT Explorer with Docker

```
version: "3"
services:
  # https://hub.docker.com/r/smeagolworms4/mqtt-explorer
  # https://github.com/Smeagolworms4/MQTT-Explorer
  # https://github.com/thomasnordquist/MQTT-Explorer
  mqtt-explorer:
    container_name: mqtt-explorer
    image: smeagolworms4/mqtt-explorer
    logging:
      driver: "json-file"
      options:
        max-size: "200k"
        max-file: "10"
    volumes:
      - /home/<your-user>/docker/mqtt-explorer/config:/mqtt-explorer/config
    ports:
      - 4000:4000
    user: "${LOCAL_USER}:${LOCAL_GROUP}"
    environment:
      - HTTP_PORT=4000
      - CONFIG_PATH=/mqtt-explorer/config
      - HTTP_USER=
      - HTTP_PASSWORD=
      - SSL_KEY_PATH=
      - SSH_CERT_PATH=
```

When the container is running, you can access MQTT Explorer via `https://<your-server/ip>:4000`
