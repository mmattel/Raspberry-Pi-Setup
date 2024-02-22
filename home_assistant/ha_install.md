# Install Home Assistant

Open source home automation that puts local control and privacy first.

## Prerequisites

### OS Agent

Install the necessary HA [os-agent](https://github.com/home-assistant/os-agent#agent-for-home-assistant-os) package for the Raspberry Pi: 

```
cd /tmp

wget https://github.com/home-assistant/os-agent/releases/download/1.6.0/os-agent_1.6.0_linux_aarch64.deb

sudo dpkg --install os-agent_1.6.0_linux_aarch64.deb
```
If you would like to uninstall because a new package has been published:
```
sudo dpkg --remove os-agent
```

### AppArmor

Add the following `apparmor=1 security=apparmor` to `/boot/cmdline.txt`.

### Docker CGroup Version

You may get a HA warning that Docker is not using [CGroup version 1](https://www.home-assistant.io/more-info/unsupported/cgroup_version/)
when using the supervised HA installation. Check with `grep cgroup /proc/filesystems` if your system supports cgroupv2. To fix using v1, add the following `systemd.unified_cgroup_hierarchy=false` to `/boot/cmdline.txt`. Also see the [HA Community Guides](https://community.home-assistant.io/t/failed-to-switch-to-cgroup-v1-error-on-manual-supervisor-install/487090/2).

Reboot when changing `/boot/cmdline.txt`.

### systemd-resolved

You may get a HA warning that `systemd-resolved` is not running. Check by issuing the following command `sudo systemctl status systemd-resolved`.
If it is not running, you can start it with `sudo systemctl start systemd-resolved`. To make it autostart, issue `sudo systemctl enable systemd-resolved`.

### systemd-journal-gatewayd

You may get a HA warning that `systemd-journal-gatewayd` is not running. Check by issuing the following command `sudo systemctl status systemd-journal-gatewayd.socket` (Note the .socket as this is required by HA). You also may get the info that it is not installed. To install it, run `sudo apt install systemd-journal-remote -y`. To make it autostart, issue `sudo ln -s /lib/systemd/system/systemd-journal-gatewayd.socket /etc/systemd/system/systemd-journal-gatewayd.socket`. This service needs some setting changes.

```
sudo mkdir /etc/systemd/system/systemd-journal-gatewayd.socket.d
sudo vi /etc/systemd/system/systemd-journal-gatewayd.socket.d/overwrite.conf
```
add

```
[Socket]
ListenStream=
ListenStream=/run/systemd-journal-gatewayd.sock
```
Then reload all services with `sudo systemctl daemon-reload` 
To start it, issue `sudo systemctl restart systemd-journal-gatewayd.socket`.
Check socket avialability with `sudo systemctl status systemd-journal-gatewayd.socket` and `ll /run/systemd-journal-gatewayd.sock`.

## Installing via Docker Compose

We use HassIO Core + Supervisor docker-compose install. The superviser docker version is a tagged one as you else would download latest which is always the dev version and not the stable one. When updating (also see the script), you define the tag you want to use for the supervisor, who then uses the latest stable image of core and other containers.

The installation is done via [docker compose](https://www.home-assistant.io/installation/linux#docker-compose).

This is the `docker-compose` file you can derive from.

Use the directory `/home/<your-user>/docker` as base for the volume.

```
services:
  hassio:
    image: ghcr.io/home-assistant/home-assistant:stable
    # https://github.com/home-assistant/core/pkgs/container/home-assistant/versions?filters%5Bversion_type%5D=tagged
    container_name: homeassistant
    logging:
      driver: journald
    privileged: true
    network_mode: host
    restart: always
    security_opt:
      - seccomp:unconfined
      - apparmor:unconfined
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - /home/mmattel/docker/hassio/config:/config
      - /var/run/docker.sock:/var/run/docker.sock
      - /var/run/dbus/system_bus_socket:/var/run/dbus/system_bus_socket:ro
      - /run/systemd-journal-gatewayd.sock:/run/systemd-journal-gatewayd.sock
    environment:
      - TZ=Europe/Vienna
    user: "${LOCAL_USER}:${LOCAL_GROUP}"
```

## Connect with MQTT

After setting up and personalizing the system you can connect HA with MQTT (mosquitto). To do so, go to `Settings > Integration > Add Integration` and add MQTT. Configure it according your mosquitto settings.

## HACS Home Assistant Community Store

HACS is necessary to install Mushroom Cards

[Download](https://hacs.xyz/docs/setup/download)

## Install Mushroom Card

[Mushroom](https://github.com/piitaya/lovelace-mushroom#installation)
