#! /bin/bash

# set -eo pipefail

# $1: ttyUSB port number

# USE AT YOUR OWN RISK
# There is absolutely NO ERROR CHECKING.

# Must be run from a valid python environment.
# The HA Docker container has all requirements installed.

# https://github.com/Koenkk/Z-Stack-firmware/blob/master/coordinator/Z-Stack_3.x.0/CHANGELOG.md
# https://github.com/Koenkk/Z-Stack-firmware/releases/download/Z-Stack_3.x.0_coordinator_20250321/CC1352P2_CC2652P_launchpad_coordinator_20250321.zip

# adapt the basepath according the needs

fw_release_date="20250321"
basepath="$HOME/sonoff_update/zb3.0p"
p_path="python"

main () {
    if [ $1 -ne 1 ]
       then
          show_usage
       else
          shift
          check_if_sonoff
          prepare_python
          prepare_python_dir
          download_serial_bootloader
          download_firmware
          flash_firmware $1
    fi
}

check_if_sonoff () {
    # check if the sonoff usb zigbee 3.0 stick is connected
    usb=$(ls -Alhr /dev/serial/by-id 2>/dev/null | \
       tr '[:upper:]' '[:lower:]')

    log

    if [ "$usb" != "${usb/sonoff}" ]; then
       log "USB has Sonoff connected"
       log
    else
       log "USB has NO Sonoff connected, exiting."
       log
       exit 1
    fi
}

prepare_python_dir() {
    mkdir -p "$basepath/$p_path"
}

download_serial_bootloader () {
    # python script that communicates with the boot loader of the
    # Texas Instruments CC2538, CC26xx and CC13xx SoCs (System on Chips)
    # https://github.com/JelmerT/cc2538-bsl
    # python script that communicates with the boot loader of the
    # Texas Instruments CC2538, CC26xx and CC13xx SoCs (System on Chips)

    cd "$basepath/$p_path"
   # code downloaded will overwrite existing one
    wget -q https://raw.githubusercontent.com/JelmerT/cc2538-bsl/refs/heads/main/cc2538_bsl/cc2538_bsl.py -O cc2538_bsl.py
    if [[ $? -ne 0 ]]; then
      log "wget download python bootloader failed"
      exit 1;
    fi
}

download_firmware () {
    # https://github.com/Koenkk/Z-Stack-firmware
    # No attempt is made to use github api to download latest versions.
    # Urls will need to be edited to point to correct files as updates
    # are posted to github.

    cd "$basepath"
    mkdir -p "${fw_release_date}"
    cd "${fw_release_date}"

    # download from release link
    wget -q https://github.com/Koenkk/Z-Stack-firmware/releases/download/Z-Stack_3.x.0_coordinator_"${fw_release_date}"/CC1352P2_CC2652P_launchpad_coordinator_"${fw_release_date}".zip -O CC1352P2_CC2652P_launchpad_coordinator_"${fw_release_date}".zip

    if [[ $? -ne 0 ]]; then
      log "wget coordinator ${fw_release_date} failed"
      exit 1;
    fi

    unzip -o CC1352P2_CC2652P_launchpad_coordinator_"${fw_release_date}".zip
}

flash_firmware () {
    # for more options see: https://github.com/JelmerT/cc2538-bsl#cc26xx-and-cc13xx
    python "$basepath/$p_path"/cc2538_bsl.py -evw -p \
        /dev/ttyUSB$1 \
        --bootloader-sonoff-usb \
        "$basepath/${fw_release_date}/CC1352P2_CC2652P_launchpad_coordinator_${fw_release_date}.hex"
}

log() {
    # the number is the color used for printing
    _log_message 3 "$@"
}

_log_message() {
    [[ -t 0 ]] && echo -ne "\e[1m\e[3${1}m"
    shift
    echo "$@"
    [[ -t 0 ]] && echo -ne "\e[0m"
}

show_usage() {
    # $1: ttyUSB port number

    log
    log "Usage: $0 [usb (ttyUSB) port number]"
    log
    log "Note that devices may not be available at all"
    log
    log "Example: /ttyUSB0 --> 0"
    log
    log USB dongles found:
    log "$(ls -Alhr /dev/serial/by-id | awk '{print $9, $10, $11}')"
    log
    log "Firmware version to be flashed: ${fw_release_date}"
    log
}

prepare_python () {
    # dependencies needed for https://github.com/JelmerT/cc2538-bsl
    # we dont use a virtual env
    log "Check python dependencies:"
    log
    dep_array=("pyserial" "intelhex" "python-magic")
    pip_array=( $(pip list | grep -v "^Package *Version$" | grep -v "^-*$" | cut -d ' ' -f 1) )

    for dep in ${dep_array[@]}; do
       echo "${pip_array[@]}" | grep -q "$dep" &&  \
          log "Already installed $dep" || \
          python3 -m pip install $dep --break-system-packages
    done
    log
}

main $# $1
