# Install Home Assistant

Open source home automation that puts local control and privacy first.

### Prerequisites

#### OS Agent

Install the necessary HA [os-agent](https://github.com/home-assistant/os-agent#agent-for-home-assistant-os) package for the Raspberry Pi: 

```
cd /tmp

wget https://github.com/home-assistant/os-agent/releases/download/1.5.1/os-agent_1.5.1_linux_aarch64.deb

sudo dpkg --install os-agent_1.5.1_linux_aarch64.deb
```
If you would like to uninstall because a new package has been published:
```
sudo dpkg --remove os-agent
```

#### AppArmor

Add the following `apparmor=1 security=apparmor` to `/boot/cmdline.txt`.

## Installing via Docker Compose

We use HassIO Core + Supervisor docker-compose install. The superviser docker version is a tagged one as you else would download latest which is always the dev version and not the stable one. When updating (also see the script), you define the tag you want to use for the supervisor, who then uses the latest stable image of core and other containers.

The installation is done via [docker compose](https://www.home-assistant.io/installation/alternative/#docker-compose).

This is the [docker-compose](https://github.com/postlund/hassio-compose/blob/master/docker-compose.yaml) file we derive from.

Use the directory `/home/<your-user>/docker` as base for the volume.

```
version: '3'
services:
  hassio:
    container_name: hassio_supervisor
    image: homeassistant/aarch64-hassio-supervisor:2023.06.3
    # image: homeassistant/armv7-hassio-supervisor:2023.06.3
    restart: always
    privileged: true
    security_opt:
      - seccomp:unconfined
      - apparmor:unconfined
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - /home/<your-user>/docker/hassio/data:/data
      - /home/<your-user>/docker/hassio/scripts:/scripts
      - /var/run/docker.sock:/var/run/docker.sock
      - /var/run/dbus/system_bus_socket:/var/run/dbus/system_bus_socket
    environment:
      # docker inspect hassio_supervisor | grep Env -A10
      - HOMEASSISTANT_REPOSITORY=homeassistant/raspberrypi4-homeassistant
      - SUPERVISOR_NAME=hassio_supervisor
      - SUPERVISOR_SHARE=/home/<your-user>/docker/hassio/data
      - DBUS_SYSTEM_BUS_ADDRESS=unix:path=/var/run/dbus/system_bus_socket
      - TZ=Europe/Vienna
    user: "${LOCAL_USER}:${LOCAL_GROUP}"
```

## Connect with MQTT

After setting up and personalizing the system you can connect HA with MQTT (mosquitto). To do so, go to `Settings > Integration > Add Integration` and add MQTT. Configure it according your mosquitto settings.

## Updating Home Assistant

To update HA, you must follow some steps in necessary order. To ease most of the steps, a script can be used. Finally, check if a new superviser has been tagged on docker hub. In case you need to update the HA supervisor compose file (stack when using portainer) and just apply the new tag on the image. When bringing the stack up, updated images are downloaded and you are up-to-date.

Open `vi ~/docker/tools/remove-hassio.sh` and copy the content of [remove-hassio.sh](../scripts/remove-hassio.sh). When done make it execuatble with `sudo chmod +x remove-hassio.sh`

Run the script, but only when HA tells you that an update is avaliable with `~/docker/tools/remove-hassio.sh`. and finalize as described above.

## HACS Home Assistant Community Store

HACS is necessary to install Mushroom Cards

[Download](https://hacs.xyz/docs/setup/download)

## Install Mushroom Card

[Mushroom](https://github.com/piitaya/lovelace-mushroom#installation)
