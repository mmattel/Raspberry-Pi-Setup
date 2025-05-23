# Raspberry-Pi-Setup

Steps to setup a RPi Server with Raspberry PI OS x64 with:

- Argon mini Fan pwm speed control
- lan0 / wlan0 failover
- Docker
- Container management with [Portainer](https://docs.portainer.io)
- Monitoring the RPi with [system_sensors](https://github.com/Sennevds/system_sensors)
- Backup your SD-Card / boot drive
- Upgrade the OS or Kernel
- Install Home Assistant

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
   * [Netplan](#netplan)
      * [Install and Configure Netplan](#install-and-configure-netplan)
   * [Install/Update Some Tools and Libraries](#installupdate-some-tools-and-libraries)
   * [Disable One-Wire GPIO](#disable-one-wire-gpio)
      * [Update the Bluetooth Driver (Bluez)](#update-the-bluetooth-driver-bluez)
      * [Install D-Bus Broker](#install-d-bus-broker)
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
      * [Portainer Add ghcr.io Registry](#portainer-add-ghcrio-registry)
   * [Live Monitoring of Docker Logs with Dozzle](#live-monitoring-of-docker-logs-with-dozzle)
   * [Install Theia IDE for RPi with Docker](#install-theia-ide-for-rpi-with-docker)
   * [Bash Script to Check a Port](#bash-script-to-check-a-port)
   * [Backup your RPi SD Card](#backup-your-rpi-sd-card)
   * [Upgrade the OS or Kernel](#upgrade-the-os-or-kernel)
   * [Full Power to USB Devices](#full-power-to-usb-devices)
   * [Summary of Ports and URL's Used](#summary-of-ports-and-urls-used)
   * [Install Home Assistant](#install-home-assistant)
      * [Steps](#steps)
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
cd /root/.vimrc .
cd /root/.bash_aliases .
vi .bashrc
```
Add the following lines at the end if not exists:

```
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi
```
Save the file and run `source ~/.profile` to enable the changes. Type `ll` to test. Finally,

```
cd /home/<your-user>
CTRL D
```

## Update Raspberry Pi OS

```
sudo apt update
sudo apt full-upgrade
sudo apt install ifupdown2 wireless-tools net-tools dnsutils lshw
sudo apt autoremove
sudo reboot
```

Check your RPi

```
sudo lshw | head -6
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

## Netplan

The goal is to create a setup where you can use eth0 and wlan0 concurrently having the same static IP address like you would have with a failover/bond but only one interface is actively used. After many trials where none of them worked, `netplan` is the solution, doing the job perfectly and is easy to configure. The `metric` entry in the yaml configuration file does the magic.

Note to configure the wireless region once like with `sudo raspi-config` to set the correct frequencies.

### Install and Configure Netplan

The interfaces will be setup so that either eth0 or wlan0 will get configured where eth0 has the higher priority than wlan0. This means that at least one but not both will get configured. If the LAN is connected, use this, but if not use the WLAN - both with the same network address making it easy to switch over without hassles.

The netplan package is available in the [debian package](https://packages.debian.org/stable/net/netplan.io) list and available to RPi.

```
sudo apt search netplan
sudo apt install netplan.io
sudo apt install openvswitch-switch-dpdk
```
After installing netplan, get the [01-netcfg.yaml](https://github.com/mmattel/Raspberry-Pi-Setup/blob/main/netplan/01-netcfg.yaml) example file, adapt it to your needs and save it in the `/etc/netplan/` folder. Note that this configuration disables IPv6 as not necessary (by the use of `link-local: [ ]`) and to reduce network startup time, but it can be enabled at any time again.

Secure the netplan config file, else you will get a complaint:
```
sudo chmod 600 01-netcfg.yaml
```

Apply the changes with following commands:
```
sudo netplan generate
sudo netplan apply
networkctl -a
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

Without being mandatory but to avoid the obligatory waiting time of 120 seconds for the interface that is not coming up, the network startup needs some adoption. Edit the `networkd wait online service` (create an override.conf) to reduce the default waiting time to 10 seconds and continue booting immediately if at least one interface is configured.

```
sudo systemctl edit systemd-networkd-wait-online
```

Add the following two lines between the comments (as described in the editor window):

```
[Service]
ExecStart=
ExecStart=/lib/systemd/systemd-networkd-wait-online --timeout=10 --any
```

Note, just use the current `ExecStart` parameter (scroll down in the editor to see the current value) and add the `timeout` and `any` option.

Use the following to check the result:

```
sudo systemctl show -p ExecStart systemd-networkd-wait-online
```

Finally reboot the Pi and monitor via console (boot process...) that there is no network wait anymore.

Additional `ExecStart` parameters can be checked via:

```
man systemd-networkd-wait-online.service
```

## Install/Update Some Tools and Libraries

```
sudo apt install netcat
sudo apt install iftop
sudo apt install libglib2.0-bin
sudo apt install build-essential
sudo apt install mtr-tiny
```

## Disable One-Wire GPIO

If you are not using the One-Wire GPIO interface, such as for the DS18B20 temperature sensor, you can safely disable it.
If it is enabled but not used, you will get many log entries when running `journalctl --system -r -a` such as:\
`kernel: w1_master_driver w1_bus_master1: Family 0 for xyz is not registered.`

To disable One-Wire GPIO run:

```bash
sudo raspi-config
```

And disable via: `5 ... Interface Options` -> `P7 - 1 Wire` --> `No`

You can see the result (or do the change manually) in:

```bash
cat /boot/config.txt
```

where `dtoverlay=w1-gpio` gets commented out. A reboot is required.

### Update the Bluetooth Driver (Bluez)

The following stelp is necessary especially when using HomeAssistant, also see [HA Bluetooth integration](https://www.home-assistant.io/integrations/bluetooth/).

The Bluetooth adapter must be accessible to D-Bus and running BlueZ >= 5.43. It is highly recommended to use BlueZ >= 5.63 as older versions have been reported to be unreliable.

Derived from [Compiling Bluez](https://learn.adafruit.com/pibeacon-ibeacon-with-a-raspberry-pi/compiling-bluez). Check on [kernel.org](www.kernel.org/pub/linux/bluetooth/) for the versions available, also see [bluez on github](https://github.com/bluez/bluez) to get the
latest stable version to download from kernel.org:

```
dpkg --status bluez | grep '^Version'
bluetoothctl -v

sudo apt update
sudo apt install build-essential
sudo apt install libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev
sudo python -m pip install docutils Pygments
cd /opt
sudo mkdir bluez
cd bluez/
sudo wget https://mirrors.edge.kernel.org/pub/linux/bluetooth/bluez-5.78.tar.xz
sudo unxz bluez-5.78.tar.xz
sudo tar xvf bluez-5.78.tar
cd bluez-5.78/
sudo ./configure --disable-cups
sudo make -j4
sudo make -j4 install

sudo systemctl daemon-reload
sudo systemctl restart dbus
(or reboot)

bluetoothctl -v

sudo bluetoothctl devices
sudo bluetoothctl connect <mac>


sudo bluetoothctl
power on
agent on
scan on
scan off
pair <mac>
paired-devices
quit
```

### Install D-Bus Broker

Similar to the above when planning to use HomeAssistant, the installation of the `dbus-broker` is adviced by HA.

First check if it is available for the distro used, the following command should return a valid entry:

```
sudo apt-cache search dbus-broker
dbus-broker - Linux D-Bus Message Broker
``` 

In case, install with `sudo apt install dbus-broker`

If the package is not available, install from [source](https://github.com/bus1/dbus-broker).

Post installation, reboot your Pi with `sudo reboot`.

## Install Python3 and pip3

Check if you have python already installed with `python -V` to show the version.

Note when using apt, this will install as of writing Python 3.9 which now EOL (just dont do it).
If it is already installed, run: `sudo apt install python3-pip` to add pip for python 3.9

```
sudo apt install python3 python3-pip
```

Install the `python3.dev` package which is sometimes required when updating a library with pip.

```
sudo apt install python3-dev
```

To install an updated version like Python 3.11 additionally if there is already a bundled OS version installed, do following steps. Note that compiling can take a while:

```
cd /tmp
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev \
  libssl-dev libsqlite3-dev tk-dev libc6-dev libbz2-dev
wget https://www.python.org/ftp/python/3.11.3/Python-3.11.3.tgz
tar -xzvf Python-3.11.3.tgz
cd Python-3.11.3/
./configure --enable-optimizations
make -j4
sudo make altinstall
pip3.11 install --upgrade pip

whereis python

sudo update-alternatives --install /usr/bin/python python /usr/local/bin/python3.11 50
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.9 30

sudo update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.11 50
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 30

sudo update-alternatives --config python
sudo update-alternatives --config python3

update-alternatives --list python
update-alternatives --list python3

whereis pip
```

Run the following to verify that you have installed the version correctly:

```
python -V
Python 3.11.1
```

Finally you can remove the files from the /temp dir:

```
rm -r /tmp/Python-3.11.1*
```

To fix an error message about a missing module `ModuleNotFoundError: No module named 'apt_pkg'` like when installing docker (see below), we need to run the following command:
```
sudo ln -s \
/usr/lib/python3/dist-packages/apt_pkg.cpython-39-aarch64-linux-gnu.so \
/usr/lib/python3/dist-packages/apt_pkg.so
```

To prepare some python packages that are often used, create a file named `requirements.txt` in your home directory with following contents, more libraries can be added easily.

```
paho-mqtt
psutil
pytz
PyYAML
rpi_bad_power
python-dotenv
docutils
RPi.GPIO
```

Note to run [check_requirements.py](./scripts/check_requirements.py) to see which of the modules are already installed.

Then load the libraries once for the user and once for root:

```
pip install -r requirements.txt
sudo pip install -r requirements.txt
```

Note that when you have selected python 3.9 via alternatives, you must load the requirements also via:

```
python -m pip install -r requirements.txt
sudo python -m pip install -r requirements.txt
```
This will make the packages available for python 3.9 too.

Also install the following, note that the provided version (2.3.0) only runs on python 3.9 and 3.10:
```
sudo apt-get install python3-dev
sudo apt-get install python3-apt
```

See [python-apt](https://salsa.debian.org/apt-team/python-apt) for how to compile an updated version

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

Install docker compose (via pip, **deprecated**):

```
docker info
sudo pip3 install docker-compose
```

Install docker compose (go, **recommended**) either via the [package manager](https://docs.docker.com/compose/install/linux/#install-using-the-repository), often outdated or [manually](https://docs.docker.com/compose/install/linux/#install-the-plugin-manually) which is latest.

Note to use the correct [architecture](https://github.com/docker/compose/releases/) for file downloading, which is for the Raspberry using a 64bit OS `aarch64` (see the ssh welcome screen).

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

Doing so, the docker service will start only if the NFS mount is available ensuring that container will work properly.
 
First of all we check if the docker servise is up, look for a positive result:

`sudo systemctl status docker`

Then check the name of the mount to wait for:

`systemctl list-units | grep -nP "\.mount"`

look for the ` home-<your-user>-docker.mount`, this mount should be present.

Add this folder to the docker service as startup dependency:

`sudo systemctl edit docker.service`

```
[Unit]
After=home-<your-user>-docker.mount
```

Then reload the daemon and check the new network dependencies with:

```
sudo systemctl daemon-reload
sudo systemctl restart docker
sudo systemctl cat docker.service
sudo systemctl show -p After docker.service
sudo systemctl show -p WantedBy network-online.target
````

Post rebooting, check the output of `/var/log/syslog` for any startup errors related to systemd changes.  

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
# sudo apt-get install apparmor-utils

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
Use `portainer-ee` for the enterprise edition.

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

### Portainer Add ghcr.io Registry

To add the ghcr.io registry to pull images, go to `Registries`, `Add registry` and `Custom registry`. Enter `ghcr.io` as `Registry URL`.
You now should be able to pull images with `image: ghcr.io/<...>`.

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

## Bash Script to Check a Port

This script checks if a port of an application responds, useful when you want to check if a service is up. The script restricts checking for local ports only.

You can put this script at any location desired, but as we use it with docker, put it in the `~/docker` directory created above.

Open `vi ~/docker/tools/port-test.sh` and copy the content of [port-test.sh](./scripts/port-test.sh). When done, make the script executable with `sudo chmod +x ~/docker/tools/port-test.sh`. Give it a try with `~/docker/tools/port-test.sh`, it is self explaining.

## Backup your RPi SD Card

To backup your SD-Card or boot drive, open `vi ~/docker/tools/make-backup.sh` and copy the content of [make-backup.sh](./scripts/make-backup.sh). When done, make the script executable with `sudo chmod +x ~/docker/tools/make-backup.sh`. Run it with `sudo ~/docker/tools/make-backup.sh`, it is self explaining.

Notes:
- The script requires the presense of the NFS mount located at `/home/<your-user>/backup` as described above.
- Rotate the amount of backup files manually to avoid wasting nfs space.
- Use [etcher](https://www.balena.io/etcher/) to burn (restore) the image to your target.

## Upgrade the OS or Kernel

For details see the: [Upgrade](./upgrading/os_upgrading.md) documentation

## Full Power to USB Devices

The RPi limits the power to USB decices. If you have a good powersupply, you can remove this restriction by editing `sudo vi /boot/config.txt` and add:

```
max_usb_current=1
```
Reboot the RPi so that the changes can take effect.

## Summary of Ports and URL's Used

| Service   | Port  | URL                              |
| :---      |  ---: | :---                             |
| Portainer | 9443  | `https:\\<your-server/ip>:9443`  |
| Dozzle    | 9999  |  `http:\\<your-server/ip>:9999`  |
| Theia     | 8100  |  `http:\\<your-server/ip>:8100`  |

## Install Home Assistant

Note, to test any USB device connected, use following command and replace ttyACM0 accordingly, like with ttyUSB0:

`test -w /dev/ttyACM0 && echo success || echo failure`

For a more detailed information use:

`udevadm info -a -n /dev/ttyACM0`

### Steps

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
| Mariadb         | 3306  | --                              |
| MQTT Explorer   | 4000  |  `http:\\<your-server/ip>:4000` |
| Zigbee2MQTT     | 8090  | `https:\\<your-server/ip>:8090` |
| ZwaveJS2mqtt    | 8091  | `https:\\<your-server/ip>:8091` |
| Adminer         | 8092  | `http:\\<your-server/ip>:8092`  |
| Home Assistant  | 8123  | `https:\\<your-server/ip>:8123` |
