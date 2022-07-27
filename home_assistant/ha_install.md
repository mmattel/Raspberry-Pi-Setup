# Install Home Assistant

Open source home automation that puts local control and privacy first.

## Installing via Docker Compose

The installation is done via [docker compose](https://www.home-assistant.io/installation/alternative/#docker-compose).

Use the directory `/home/<your-user>/docker` as base for the volume.

```
version: '3'
services:
  homeassistant:
    container_name: homeassistant
    image: "ghcr.io/home-assistant/home-assistant:stable"
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "200k"
        max-file: "10"
    volumes:
      - //home/<your-user>/docker/hass:/config
      - /etc/localtime:/etc/localtime:ro
    privileged: true
    network_mode: host
```

https://github.com/home-assistant/os-agent/releases/
wget https://github.com/home-assistant/os-agent/releases/download/1.2.2/os-agent_1.2.2_linux_armv7.deb
sudo dpkg --install os-agent_1.2.2_linux_armv7.deb
sudo dpkg --remove os-agent

HassIO Supervisor Install

```
version: '3'
services:
  hassio:
    # image: homeassistant/aarch64-hassio-supervisor
    image: homeassistant/armv7-hassio-supervisor
    # image: homeassistant/arm64-hassio-supervisor
    container_name: hassio_supervisor
    privileged: true
    restart: always
    security_opt:
      - seccomp:unconfined
      - apparmor:unconfined
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - /home/mmattel/docker/hassio/data:/data
      - /home/mmattel/docker/hassio/scripts:/scripts
      - /var/run/docker.sock:/var/run/docker.sock
      - /var/run/dbus/system_bus_socket:/var/run/dbus/system_bus_socket
    environment:
      # docker inspect hassio_supervisor | grep Env -A10
      - HOMEASSISTANT_REPOSITORY=homeassistant/raspberrypi4-homeassistant
      - SUPERVISOR_NAME=hassio_supervisor
      - SUPERVISOR_SHARE=/home/mmattel/docker/hassio/data
      - DBUS_SYSTEM_BUS_ADDRESS=unix:path=/var/run/dbus/system_bus_socket
      - TZ=Europe/Vienna
    user: "${LOCAL_USER}:${LOCAL_GROUP}"
```

https://hub.docker.com/r/homeassistant/raspberrypi4-homeassistant

https://community.home-assistant.io/t/home-assistant-docker-not-accessible/366963/3

```
services:
  homeassistant:
    container_name: homeassistant
    image: ghcr.io/home-assistant/raspberrypi4-homeassistant:latest
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - /etc/timezone:/etc/timezone:ro
      - /opt/docker/homeassistant:/config
    restart: unless-stopped
    network_mode: host
```

[Official Zigbee2MQTT Home Assistant addon](https://www.zigbee2mqtt.io/guide/installation/03_ha_addon.html#home-assistant-addon)
