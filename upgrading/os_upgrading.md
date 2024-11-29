# Upgrading the OS

To upgrade the OS like from Debian 11 (bullseye) to Debian 12 (bookworm), follow the steps described:

* Check the version:
  ```bash
  cat /etc/os-release
  ```
* Update apt packages:
  ```bash
  sudo apt update && sudo apt upgrade -y
  sudo apt dist-upgrade
  ```
* Upgrade the Raspberry Pi firmware:
  ```bash
  sudo rpi-update
  ```
* Edit source list:
  ```bash
  sudo sed -i "s/bullseye/bookworm/g" /etc/apt/sources.list
  sudo sed -i "s/bullseye/bookworm/g" /etc/apt/sources.list.d/raspi.list
  ```
  Note, change this on other sources too...\
  Add `contrib` and `non-free-firmware` after main in `/etc/apt/sources.list`:\
  `deb http://deb.debian.org/debian/ bookworm main contrib non-free-firmware`

* Update all packages from bullseye to bookworm:
  ```bash
  sudo apt update
  sudo apt dist-upgrade
  sudo apt update && sudo apt upgrade -y
  sudo apt autoremove -y && sudo apt autoclean -y
  ```
* Reboot to apply changes:
  ```bash
  sudo reboot
  ```

* Check the version:
  ```bash
  cat /etc/os-release
  ```
