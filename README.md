# Raspberry-Pi-Setup
Steps to setup a RPi Server with Raspberry PI OS x64

## Install the Raspberry Pi OS x64 Server Image

## Prerequisites

- RPi
- HDMI cable + Monitor
- USB keyboard
- A DHCP server must be available to provide an IP address for your RPi. 

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
