# Install Home Assistant

Open source home automation that puts local control and privacy first.

### Prerequisites

Install the necessary HA [os-agent](https://github.com/home-assistant/os-agent#agent-for-home-assistant-os) package for the Raspberry Pi: 

```
cd /tmp

wget https://github.com/home-assistant/os-agent/releases/download/1.3.0/os-agent_1.3.0_linux_armv7.deb

sudo dpkg --install os-agent_1.3.0_linux_armv7.deb
```
If you would like to uninstall because a new package has been published:
```
sudo dpkg --remove os-agent
```

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
    image: homeassistant/armv7-hassio-supervisor:2022.08.3
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

## Updating Home Assistant

To update HA, you must follow some steps in necessary order. To ease most of the steps, a script can be used. Finally, check if a new superviser has been tagged on docker hub. In case you need to update the HA supervisor compose file (stack when using portainer) and just apply the new tag on the image, When bringing the stack up, updated images are downloaded and you are up-to-date.

Create a file named `<you-user>/docker/tools/remove-hassio.sh` and make it execuatble with `sudo chmod +x remove-hassio.sh`:

```
#! /bin/bash

echo "stopping the HA supervisor container"
container1=$(docker container ls --format="{{.Image}} {{.ID}}" |
grep "hassio-supervisor" | cut -d' ' -f2)
#echo $container1
if [ "$container" ]; then
  docker stop $container1
  docker wait $container1
fi

echo "stop the remaining HA containers, waiting"
container2=$(docker container ls --format="{{.Image}} {{.ID}}" |
grep "hassio\|home-assistant" | cut -d' ' -f2)

container2=$(echo ${container2//$container1/} | xargs)
#echo $container2
if [ "$container2" ]; then
  docker stop $container2
  docker wait $container2
fi
#exit

echo "remove all HA containers"
container3=$(docker images --format="{{.Repository}} {{.ID}}" |
grep "hassio\|homeassistant" | cut -d' ' -f2)

if [ "$container3" ]; then
  docker rmi -f $container3
fi

echo

# print the remaining images to proof image deletion
docker images

echo
echo "check: https://hub.docker.com/r/homeassistant/armv7-hassio-supervisor/tags?page=1"
echo "to get the latest stable supervisor tag (not latest or .devxxx)"
```

## Connect with MQTT

After setting up and personalizing the system you can connect HA with MQTT (mosquitto). To do so, go to `Settings > Integration > Add Integration` and add MQTT. Configure it according your mosquitto settings.
