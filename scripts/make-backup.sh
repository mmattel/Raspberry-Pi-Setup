#!/bin/bash

# Make sure only root can run this script
if [ "$(id -u -n)" != "root" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

main () {
echo "creating a backup image"
echo "running..."
echo
sudo dd if=/dev/mmcblk0p1 bs=32M | bzip2 --best > /home/mmattel/backup/$(date +%Y%m%d_%H%M%S)_backup_$(hostname).bz2
}

time main

echo
echo "use https://www.balena.io/etcher/ to burn the image to disk"

