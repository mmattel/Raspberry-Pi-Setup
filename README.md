# Raspberry-Pi-Setup
Steps to setup a RPi Server with Raspberry PI OS x64

Table of Contents
=================

   * [Prerequisites](#prerequisites)
   * [Install the Raspberry Pi OS x64 Server Image](#install-the-raspberry-pi-os-x64-server-image)
      * [Raspberry Pi Imager](#raspberry-pi-imager)
   * [Base Preparation](#base-preparation)
      * [Install vim](#install-vim)
         * [Set bash_aliases](#set-bash_aliases)
   * [Update Raspberry Pi OS](#update-raspberry-pi-os)
   * [wlan0 (for testing only, eg without eth0 connected)](#wlan0-for-testing-only-eg-without-eth0-connected)
   * [Netplan (RaspOS Bullseye)](#netplan-raspos-bullseye)
      * [Install and Configure Netplan](#install-and-configure-netplan)
   * [Install Python3 and pip3](#install-python3-and-pip3)
   * [Enable Argon Mini Fan temp driven PWM fan speed](#enable-argon-mini-fan-temp-driven-pwm-fan-speed)
      * [PWM controlled fan speed](#pwm-controlled-fan-speed)
      * [Check the Fan Speed](#check-the-fan-speed)
      * [Making fan_control a Service](#making-fan_control-a-service)

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

Do a `ping www.google.com` to see if you have a internet connection.

## Base Preparation

### Install vim

`sudo apt install vim`

#### Set bash_aliases

`nano ~/.bash_aliases`

add:
```
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
```
use the new settings:

`source ~/.profile`

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
…copy psk to /etc/wpa_supplicant/wpa_supplicant.conf

…add scan_ssid=1 if you have a hidden SSID

Enable wlan0 on boot

```
sudo cp /etc/wpa_supplicant/wpa_supplicant.conf /boot
sudo reboot
```
`ip -br addr show`

## Netplan (RaspOS Bullseye)

The goal is to create a setup where you can use eth0 and wlan0 concurrently having the same static IP address like you would have with a failover/bond but only one interface is actively used. After many trials where none of them worked, `netplan` is the solution, doing the job perfectly and is easy to configure. The `metric` entry does the magic.

### Install and Configure Netplan

The netplan package is available in the [debian package](https://packages.debian.org/stable/net/netplan.io) list and available to RPi.

```
sudo apt search netplan
sudo apt install netplan.io
```
After installing netplan, see the [01-netcfg.yaml](https://github.com/mmattel/Raspberry-Pi-Setup/blob/main/netplan/01-netcfg.yaml) example file, adapt it to your needs and save it in the `/etc/netplan/` folder.

Apply the following commands:
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

## Install Python3 and pip3

```
sudo apt install python3 python3-pip
```

## Enable Argon Mini Fan temp driven PWM fan speed

Note, **do not use the argonone.sh** script. It is not designed for that fan and will not work.

Note, you can of course set a fixed temp value in `/boot/config.txt` like `dtoverlay=gpio-fan,gpiopin=18,temp=65000`, but you only get on/off and lose fan speed control, with a fan that offers PWM...   

Note that the Argon mini Fan uses GPIO pin 18 for PWM speed control.

### PWM controlled fan speed

Create a folder in your home directory and copy the following files to this location, you can change it according your needds, adopt the file/path in `fan_control.service` accordingly:

`mkdir ~/fan_control`

[calib_fan.py](https://github.com/mmattel/Raspberry-Pi-Setup/blob/main/fan_control/calib_fan.py)

[fan_control.py](https://github.com/mmattel/Raspberry-Pi-Setup/blob/main/fan_control/fan_control.py)

[fan_control.service](https://github.com/mmattel/Raspberry-Pi-Setup/blob/main/fan_control/fan_control.service)

While not mandatory, it is g good thing to check the minimum required value to turn on the fan speed.

To do so, configure the `calib_fan.py` script to identify the minimum speed. Use a low temperature so you can see it immediately. Check other values too.

Note that you mandatory need minimum temperature value with zero speed which is reached when cooling down, else the fan will turn forever when turned on once.

Use the minimum fan speed value and configure the `fan_control.py` script, set the temp/speed values according your needs.

### Check the Fan Speed

Open two terminals, T1 and T2

In T1, we check if the `fan_control.py` script is working, type `python3 fan_control.py`

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

You may use different stress tests too.

### Making fan_control a Service

```
sudo systemctl link /home/<your-user>/fan_control/fan_control.service
sudo systemctl daemon-reload
sudo systemctl enable fan_control
sudo systemctl start fan_control.service
sudo systemctl status fan_control.service
```
