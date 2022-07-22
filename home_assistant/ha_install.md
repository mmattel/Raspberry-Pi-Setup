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
    logging:
      driver: "json-file"
      options:
        max-size: "200k"
        max-file: "10"
    volumes:
      - //home/<your-user>/docker/hass:/config
      - /etc/localtime:/etc/localtime:ro
    restart: unless-stopped
    privileged: true
    network_mode: host
```
