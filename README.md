# Raspberry-Pi-Setup

Steps to setup a RPi Server with Raspberry PI OS x64 with:

- Argon mini Fan pwm speed control
- lan0 / wlan0 failover
- Docker
- Container management with [Portainer](https://docs.portainer.io)
- Monitoring the RPi with [netdata](https://learn.netdata.cloud)

Table of Contents
=================

   * [Prerequisites](#prerequisites)
   * [Install the Raspberry Pi OS x64 Server Image](#install-the-raspberry-pi-os-x64-server-image)
      * [Raspberry Pi Imager](#raspberry-pi-imager)
   * [Base Preparation](#base-preparation)
      * [Install and Configure vim](#install-and-configure-vim)
      * [Set bash_aliases](#set-bash_aliases)
      * [Use bash and vim Settings for Root](#use-bash-and-vim-settings-for-root)
   * [Update Raspberry Pi OS](#update-raspberry-pi-os)
   * [wlan0 (for testing only, eg without eth0 connected)](#wlan0-for-testing-only-eg-without-eth0-connected)
   * [Netplan (RaspOS Bullseye)](#netplan-raspos-bullseye)
      * [Install and Configure Netplan](#install-and-configure-netplan)
   * [Install Some Tools and Libraries](#install-some-tools-and-libraries)
   * [Install Python3 and pip3](#install-python3-and-pip3)
   * [Enable Argon Mini Fan temp driven PWM fan speed](#enable-argon-mini-fan-temp-driven-pwm-fan-speed)
      * [PWM controlled fan speed](#pwm-controlled-fan-speed)
      * [Check the Fan Speed](#check-the-fan-speed)
      * [Making fan_control a Service](#making-fan_control-a-service)
   * [Install and Configure the NFS Client](#install-and-configure-the-nfs-client)
   * [Installing Docker and Docker Compose](#installing-docker-and-docker-compose)
      * [Setup Docker to Wait for NFS Mounts](#setup-docker-to-wait-for-nfs-mounts)
   * [Installing Podman](#installing-podman)
   * [Installing Portainer with Docker](#installing-portainer-with-docker)
      * [Portainer Container Admin Password Reset](#portainer-container-admin-password-reset)
      * [Portainer Upgrade](#portainer-upgrade)
   * [Live Monitoring of Docker Logs with Dozzle](#live-monitoring-of-docker-logs-with-dozzle)
   * [Install Theia IDE for RPi with Docker](#install-theia-ide-for-rpi-with-docker)
   * [Install Netdata with Docker](#install-netdata-with-docker)
   * [Bash Script to Check a Port](#bash-script-to-check-a-port)
   * [Summary of Ports and URL's Used](#summary-of-ports-and-urls-used)
   * [Install Home Assistant](#install-home-assistant)
      * [Additional Ports and URL's Used](#additional-ports-and-urls-used)

<!-- Created by https://github.com/ekalinin/github-markdown-toc -->

## Prerequisites

- RPi
- Poly+ case with Argon mini Fan (HAT, PWM enabled)
- HDMI cable + Monitor
- USB keyboard
- A DHCP server must be available to provide an IP address for your RPi for first configuration.

## Install the Raspberry Pi OS x64 Server Image

### Raspberry Pi Imager

Download the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) and prepare your micro SD card with the Raspberry Pi OS x64 server image. You also can use the desktop version if you want...

When finished, insert the card in your PI, connect your LAN port and power up. Watch the booting process on the monitor.

Do a `ping www.google.com` to see if you have an internet connection.

## Base Preparation

### Install and Configure vim

`sudo apt install vim`

Add following lines to `~/.vimrc`, create one if it does not exist:

```
set encoding=utf-8
set showmode
set backspace=indent,eol,start
set clipboard+=unnamed  " use the clipboards of vim and win
set paste               " Paste from a windows or from vim
set go+=a               " Visual selection automatically copied to the clipboard
set mouse=r             " enable mouse copy/paste
syntax on               " permanently turn on syntax highlighting
```

### Set bash_aliases

`nano ~/.bash_aliases`

add:
```
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
```
use the new settings:

`source ~/.profile`

### Use bash and vim Settings for Root

Use the same bash settings from your user also when using root.

```
sudo su -
cd /root
cd /home/<your-user>/.vimrc .
cd /home/<your-user>/.bash_aliases .
cd /home/<your-user>
```

## Update Raspberry Pi OS

```
sudo apt update
sudo apt full-upgrade
sudo apt install ifupdown2 wireless-tools net-tools dnsutils
sudo apt autoremove
sudo reboot
```

## wlan0 (for testing only, eg without eth0 connected)

```
sudo wpa_passphrase [ssid-name] [password-name]
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```
… copy the psk key to /etc/wpa_supplicant/wpa_supplicant.conf

… add scan_ssid=1 if you have a hidden SSID

Enable wlan0 on boot

```
sudo cp /etc/wpa_supplicant/wpa_supplicant.conf /boot
sudo reboot
```
`ip -br addr show`

## Netplan (RaspOS Bullseye)

The goal is to create a setup where you can use eth0 and wlan0 concurrently having the same static IP address like you would have with a failover/bond but only one interface is actively used. After many trials where none of them worked, `netplan` is the solution, doing the job perfectly and is easy to configure. The `metric` entry in the yaml configuration file does the magic.

### Install and Configure Netplan

The netplan package is available in the [debian package](https://packages.debian.org/stable/net/netplan.io) list and available to RPi.

```
sudo apt search netplan
sudo apt install netplan.io
```
After installing netplan, get the [01-netcfg.yaml](https://github.com/mmattel/Raspberry-Pi-Setup/blob/main/netplan/01-netcfg.yaml) example file, adapt it to your needs and save it in the `/etc/netplan/` folder.

Apply the changes with following commands:
```
sudo netplan generate
sudo netplan apply
ip -br addr show
```

If you have configured the wlan0 interface before, **REMOVE** wlan0 from `wpa supplicant`.

```
sudo wpa_cli remove_network 0
sudo wpa_cli save_config
```
Disable `dhcpcd` for `eth0` and `wlan0` to avoid that the interfaces get an additional dynamic IP address beside the static one if connected. 

`sudo vi /etc/dhcpcd.conf` 

Set `denyinterfaces eth0 wlan0`, save and restart the dhcpcd service. The interfaces will now no longer show up a second dynamic provided IP address.

```
sudo systemctl restart dhcpcd
ip -br addr show
```

## Install Some Tools and Libraries

```
sudo apt install netcat
sudo apt install iftop
sudo apt install libglib2.0-bin
sudo apt install build-essential
```

## Install Python3 and pip3

```
sudo apt install python3 python3-pip
```

## Enable Argon Mini Fan temp driven PWM fan speed

Note, **do not use the argonone.sh** script. It is not designed for that fan and will not work.

Note, you can of course set a fixed temp value in `/boot/config.txt` like

`dtoverlay=gpio-fan,gpiopin=18,temp=65000`

but you only get on/off and lose fan speed control, having a fan that offers PWM...   

Note that the Argon mini Fan uses GPIO pin 18 for PWM speed control.

### PWM controlled fan speed

Kudos for this aricle as source, some adoptions made [PWM Regulated Fan Based on CPU Temperature](https://www.instructables.com/PWM-Regulated-Fan-Based-on-CPU-Temperature-for-Ras/)

Create a folder in your home directory and copy the following files to this location, you can change it according your needs, adopt the file/path in `fan_control.service` accordingly:

`mkdir ~/fan_control`

[calib_fan.py](https://github.com/mmattel/Raspberry-Pi-Setup/blob/main/fan_control/calib_fan.py)

[fan_control.py](https://github.com/mmattel/Raspberry-Pi-Setup/blob/main/fan_control/fan_control.py)

[fan_control.service](https://github.com/mmattel/Raspberry-Pi-Setup/blob/main/fan_control/fan_control.service)

While not mandatory, it is g good thing to check the minimum speed required value to turn on the fan.

To do so, configure the `calib_fan.py` script to identify the minimum speed. Use a low temperature so you can see it immediately. Check other values too.

Note that you mandatory need a minimum temperature / zero speed value pair which is reachable when cooling down, else the fan will turn forever if it turns on once.

Use the minimum fan speed value and configure the `fan_control.py` script, set/change the temp/speed value pairs according your needs.

### Check the Fan Speed

Open two terminals, T1 and T2

In T1, start with `python3 fan_control.py` the script to see if it is working

In T2, we do a stress test:

```
sudo apt install stress
vcgencmd measure_temp
.local/bin/stressberry-run out.dat
```

The test takes about 5min, the fan speed should change from 0 to what you have set and back to 0. If you have a gui, you can create from the data a plot to be viewed:

```
.local/bin/stressberry-plot out.dat -o out.png
```

You may use different stress tests too. Change the temp / speed pairs if necessary and redo the test.

### Making fan_control a Service

When you are satisified with the result, make `fan_control.py` a service.

Set `<your-user>` according your username. Check in `fan_control.service` if you have set the path to `fan_control.py` correctly. 

```
sudo systemctl link /home/<your-user>/fan_control/fan_control.service
sudo systemctl daemon-reload
sudo systemctl enable fan_control
sudo systemctl start fan_control.service
sudo systemctl status fan_control.service
```

## Install and Configure the NFS Client

NFS is used to store the `docker` and the `backup` folder in the home directory. This is done to relax the IO from the SD card improving its lifetime.

* The `docker` folder will contain all volumes used by containers. 
* The `backup` folder will contain the RPi backup image.

`sudo apt install nfs-common`

Add to your `/etc/fstab` the following lines, the `_netdev` option waits until the network is up, `nofail` continues the boot process without being stuck when the mount is not available.

`sudo vi /etc/fstab`

```
# nfs
<nfs-server>:path_docker /home/<your-user>/docker nfs bg,nfsvers=3,wsize=32768,rsize=32768,tcp,_netdev,nofail 0 0
<nfs-server>:path_backup /home/<your-user>/backup nfs bg,nfsvers=3,wsize=32768,rsize=32768,tcp,_netdev,nofail 0 0
```

Run `sudo mount -a` to mount all directories.

## Installing Docker and Docker Compose

Note that installing docker may take some minutes.

```
sudo apt update
sudo apt upgrade
sudo curl -fsSL https://get.docker.com get-docker.sh | bash
sudo usermod -aG docker ${USER}
```

Logout your terminal session and relogin to apply the usermod changes.

Install docker compose:

```
docker info
sudo pip3 install docker-compose
```

Allow the Docker System Service to Launch your Containers on Boot:

`sudo systemctl enable docker`

Create a default docker base directory for all your volumes you want to access:

`mkdir -p ~/docker`

Create an own file in `/etc/profiles.d` to define global environment variables used by containers or compose.

`sudo vi /etc/profiles.d/docker-env.sh`

Add at the following to define following environment variables:
```
export LOCAL_USER=1000
export LOCAL_GROUP=1000
```

Reload your environment settings with (both are necessary to get back your settings for bash):

```
source /etc/profile
source ~/.profile
```

Note if you want to remove an envoronment variable, just call `unset <variable-name>`.

### Setup Docker to Wait for NFS Mounts

Doing so, the service will start only if the NFS mount is available ensuring that container will work properly.
 
First of all we check if the docker servise is up, look for a positive result:

`sudo systemctl status docker`

Then check the name of the mount to wait for:

`systemctl list-units | grep -nP "\.mount"`

look for the ` home-<your-user>-docker.mount`, this mount should be present.

Add this folder to the docker service as startup dependency:

`sudo systemctl edit docker.service`

```
[UNIT]
After=home-mmattel-docker.mount
```

## Installing Podman

If you want to use podman...

```
sudo apt install podman
sudo vi /etc/containers/registries.conf
```
Set the string: `unqualified-search-registries = ["docker.io"]`

## Installing Portainer with Docker

With portainer, you can easily deploy, configure and secure containers in minutes with a nice GUI.

[Portainer](https://docs.portainer.io/start/install/server/docker/linux) consists of two elements, the **Portainer Server**, and the **Portainer Agent** when using a client. Both elements run as lightweight Docker containers on a Docker engine.

This document will help you install the **Portainer Server** container on your Linux environment.

```
docker volume create portainer_data

docker run \
  -d \
  -p 8000:8000 \
  -p 9443:9443 \
  --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data portainer/portainer-ce:latest
```

When the Portainer Container is running, access it with: `https://<your-server/ip>:9443`

Note that on first login, an admin user is created requiring a **12 digit** password. You can change this setting (and afterwards the pwd for the admin user) by going to **Settings > Authentication > Password rules**.

### Portainer Container Admin Password Reset

If you have forgotten the main admin password and no other admin user exists...
  
```
docker container stop portainer
docker run --rm -v portainer_data:/data portainer/helper-reset-password

docker container start portainer
```

### Portainer Upgrade

Follow the [portainer upgrade documantation](https://docs.portainer.io/start/upgrade/docker) for details.

## Live Monitoring of Docker Logs with Dozzle

Altough you can access the logs in Portainer, it is not that eyecatching _click-and-go_ as with [Dozzle](https://golangexample.com/a-web-based-interface-to-monitor-your-docker-container-logs-live/). Dozzle is a simple, lightweight application that provides you with a web based interface to monitor your Docker container logs live. It doesn’t store log information, it is for live monitoring of your container logs only. You also can find Dozzle on [GitHub](https://github.com/amir20/dozzle).

```
version: "3"
services:
  dozzle:
    container_name: dozzle
    image: amir20/dozzle:latest
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "200k"
        max-file: "10"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    ports:
      - 9999:8080
    environment:
      - DOZZLE_LEVEL=info
      # - DOZZLE_NO_ANALYTICS=true # uncomment to disallow statistics
```

When Dozzle is running, access it with: `https://<your-server/ip>:9999`


## Install Theia IDE for RPi with Docker

The official Theia docker image is designed forAMD64 architectures, the common one that powers laptops and desktop PCs. In this case we are going to use a custom image to extend the compatibility to ARM devices like Raspberry Pi. Sourced from [Deploying Theia with Docker in Raspberry Pi](https://brjapon.medium.com/part-3-deploying-theia-ide-using-docker-740f8e2de841)

To maintain the container via Portainer, add a new container via the Portainer GUI with the data as shown below. Change the port (8100) as required by your envronment.

```
version: "3"
services:
  theia:
    container_name: theia
    image: brjapon/theia-arm64
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "200k"
        max-file: "10"
    volumes:
      - /home/<your username>:/home/project
    ports:
      - 8100:3000
```

When finished, you can access the Theia IDE via `https://<your-server/ip>:8100`

## Install Netdata with Docker

Netdata is a monitoring, visualization, and troubleshooting solution for systems, containers, services, and applications.

While the product is great, the [netdata docker documentation](https://learn.netdata.cloud/docs/agent/packaging/docker) has some room for improvement. The following is a working setup description.

Prepare a `netdata` directory in your home:

`mkdir -p ~/netdata`

Use this base path for the mounts described in [Install Netdata with Docker](https://learn.netdata.cloud/docs/agent/packaging/docker) compose file, use Portainer Stack to compose the container. Note that it was necessary to add the DOCKER_USR/GRP info, else the container errored with can't write into `/var/cache/netdata`. See the [Github](https://github.com/netdata/netdata/issues/8663) issue for this.

First we need to make a [Host editable configuration](https://learn.netdata.cloud/docs/agent/packaging/docker#host-editable-configuration)

```
sudo mkdir -p /usr/lib/netdata
sudo chown <your-user>:<your-user> /usr/lib/netdata
docker run -d --name netdata_tmp netdata/netdata
docker cp netdata_tmp:/usr/lib/netdata/conf.d /usr/lib/netdata/
docker rm -f netdata_tmp
```

Use the following composer file for netdata and adapt it to your needs:

```
version: '3'
services:
  netdata:
    container_name: netdata
    image: netdata/netdata
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "200k"
        max-file: "10"
    hostname: <your-hostname> # set to fqdn of host
    ports:
      - 19999:19999
    cap_add:
      - SYS_PTRACE
    security_opt:
      - apparmor:unconfined
    volumes:
      - /home/<your-user>/docker/netdata/config:/etc/netdata
      - /home/<your-user>/docker/netdata/lib:/var/lib/netdata
      - /home/<your-user>/docker/netdata/cache:/var/cache/netdata
      - /etc/passwd:/host/etc/passwd:ro
      - /etc/group:/host/etc/group:ro
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /etc/os-release:/host/etc/os-release:ro
    environment:
      - DOCKER_USR=1000
      - DOCKER_GRP=1000
```

When the container is running, you can access netdata via `https://<your-server/ip>:19999`

To make `edit-config` work, you need to set the needed environment variables when using docker.

Add at the following to define the necessary environment variables for `edit-config`. Note it needs the full path and no substitution and you must set the env's in `/etc/profiles.d/docker-env.sh` and not in `~/.bashrc`:

`sudo vi /etc/profiles.d/docker.sh`

```
export NETDATA_USER_CONFIG_DIR="/home/<your-username>/docker/netdata/config"
export NETDATA_STOCK_CONFIG_DIR="/home/<your-username>/docker/netdata/config/orig"
```

Reload your environment settings with (both are necessary to get back your settings for bash):

```
source /etc/profile
source ~/.profile
```
Check if the environment variables are present with:

`printenv | grep NETDATA`

To see if it is working, run `sudo ~/netdata/netdataconfig/edit-config`.

Check the output for the `Stock` and `User` config location with following command. You also should see the listing of the available config files.

[Enable temperature sensor monitoring](https://learn.netdata.cloud/guides/monitor/pi-hole-raspberry-pi#enable-temperature-sensor-monitoring) for yor RPi

`sudo ~/netdata/netdataconfig/edit-config charts.d.conf`

Uncomment `# sensors=force` --> `sensors=force`

Restart the container, and see the RPi temperature in the web interface in section `Sensors`.

## Bash Script to Check a Port

This script checks if a port of an application responds, useful when you want to check if a service is up. The script restricts checking for local ports only.

You can put this script at any location desired, but as we use it with docker, put it in the `~/docker` directory created above.

Open `vi ~/docker/port-test.sh` and copy the content of [port-test.sh](./scripts/port-test.sh). When done, make the script executable with `sudo chmod +x ~/docker/port-test.sh`. Give it a try with `~/docker/port-test.sh`, it is self explaining.

<!---
/api/v1/chart?
URL/dashboard.html
https://github.com/netdata/netdata/issues/9144
-->

## Summary of Ports and URL's Used

| Service   | Port  | URL                              |
| :---      |  ---: | :---                             |
| Portainer | 9443  | `https:\\<your-server/ip>:9443`  |
| Dozzle    | 9999  |  `http:\\<your-server/ip>:9999`  |
| Theia     | 8100  |  `http:\\<your-server/ip>:8100`  |
| netdata   | 19999 |  `http:\\<your-server/ip>:19999` |

## Install Home Assistant

Note, to test any USB device connected, use following command and replace ttyACM0 accordingly, like with ttyUSB0:

`test -w /dev/ttyACM0 && echo success || echo failure`

For a more detailed information use:

`udevadm info -a -n /dev/ttyACM0`

- Install [Mosquitto](./home_assistant/mosquitto.md)
- Install [MQTT Explorer](./home_assistant/mqtt_explorer.md)
- Install [Zigbee2MQTT](./home_assistant/zigbee2mqtt.md)
- Install [ZwaveJS2mqtt](./home_assistant/zwavejs2mqtt.md)
- Install [Mariadb](./home_assistant/mariadb.md)
- Install [Adminer](./home_assistant/adminer.md)
- Install [Home Assistant](./home_assistant/ha_install.md)

### Additional Ports and URL's Used

| Service         | Port  | URL                             |
| :---            |  ---: | :---                            |
| Mosquitto       | 1883  | --                              |
| MQTT Explorer   | 4000  |  `http:\\<your-server/ip>:4000` |
| Zigbee2MQTT     | 8090  | `https:\\<your-server/ip>:8090` |
| ZwaveJS2mqtt    | 8091  | `https:\\<your-server/ip>:8091` |
| Mariadb         | 3306  | --                              |
| Adminer         | 8092  | `http:\\<your-server/ip>:8092`  |
| Home Assistant  | 8123  | `https:\\<your-server/ip>:8123` |
