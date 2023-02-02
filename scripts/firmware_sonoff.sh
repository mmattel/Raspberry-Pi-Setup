#! /bin/bash

# set -eo pipefail

# $1: dev or master
# $2: router or coordinator
# $3: ttyUSB port number

# USE AT YOUR OWN RISK
# There is absolutely NO ERROR CHECKING.

# Must be run from a valid python environment.
# The HA Docker container has all requirements installed.

# adapt the basepath according the needs
basepath="$HOME/docker/tools/sonoff-zb3.0p"
tmp="tmp"

main () {
    if [ $1 -ne 4 ]
       then
          show_usage
       else
          shift
          check_if_sonoff
          prepare_python
          prepare_tmp_dir
          download_serial_bootloader
          download_firmware $1 $2
          flash_firmware $1 $2 $3 $4
          cleanup
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

prepare_tmp_dir() {
    rm -rf $basepath/$tmp
    mkdir -p $basepath/$tmp
}

download_serial_bootloader () {
    # python script that communicates with the boot loader of the
    # Texas Instruments CC2538, CC26xx and CC13xx SoCs (System on Chips)
    # https://github.com/JelmerT/cc2538-bsl
    # python script that communicates with the boot loader of the
    # Texas Instruments CC2538, CC26xx and CC13xx SoCs (System on Chips)

    cd $basepath/$tmp
    wget https://github.com/JelmerT/cc2538-bsl/raw/master/cc2538-bsl.py
    if [[ $? -ne 0 ]]; then
      log "wget download python bootloader failed"
      exit 1;
    fi
}

download_firmware () {
    # https://github.com/Koenkk/Z-Stack-firmware
    # No attempt is made to use github api to download latest versions.
    # Urls may need to be edited to point to correct files as updates are posted to github.

    if [ $1 == "master" ]; then
      cd $basepath/$tmp
      mkdir master
      cd master

      # Master branch coordinator
      if [ $2 == "coordinator" ]; then
        wget https://github.com/Koenkk/Z-Stack-firmware/raw/master/coordinator/Z-Stack_3.x.0/bin/CC1352P2_CC2652P_launchpad_coordinator_$4.zip

        if [[ $? -ne 0 ]]; then
          log "wget $1 coordinator failed"
          exit 1;
        fi
      fi

      if [ $2 == "router" ]; then
        wget https://github.com/Koenkk/Z-Stack-firmware/raw/master/router/Z-Stack_3.x.0/bin/CC1352P2_CC2652P_launchpad_router_$4.zip

        if [[ $? -ne 0 ]]; then
          log "wget $1 router failed"
          exit 1;
        fi
      fi

      for f in *.zip; do unzip $f; done
    fi

    if [ $1 == "dev" ]; then
      cd $basepath/$tmp
      mkdir dev
      cd dev

      # Dev branch coordinator
      if [ $2 == "coordinator" ]; then
        wget https://github.com/Koenkk/Z-Stack-firmware/raw/develop/coordinator/Z-Stack_3.x.0/bin/CC1352P2_CC2652P_launchpad_coordinator_$4.zip

        if [[ $? -ne 0 ]]; then
          log "wget $1 coordinator failed"
          exit 1;
        fi
      fi

      if [ $2 == "router" ]; then
        wget https://github.com/Koenkk/Z-Stack-firmware/raw/develop/router/Z-Stack_3.x.0/bin/CC1352P2_CC2652P_launchpad_router_$4.zip

        if [[ $? -ne 0 ]]; then
          log "wget $1 router failed"
          exit 1;
        fi
      fi

      for f in *.zip; do unzip $f; done
    fi
}

flash_firmware () {
    # for more options see: https://github.com/JelmerT/cc2538-bsl#cc26xx-and-cc13xx
    python $basepath/$tmp/cc2538-bsl.py -evw -p \
        /dev/ttyUSB$3 \
        --bootloader-sonoff-usb \
        $basepath/$tmp/$1/*$2*.hex
}

cleanup () {
    rm -rf $basepath/$tmp
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
    # $1: dev or master
    # $2: router or coordinator
    # $3: ttyUSB port number
    # $4: the filename date component like 20221226

    log
    log "Usage: $0 [branch] [type] [usb port number]"
    log
    log "branch:  master or dev"
    log "type:    coordinator or router"
    log "port:    ttyUSB port number"
    log "date:    filename date component"
    log
    log "Note that dev of router may not be available at all"
    log "Example: /ttyUSB0 --> 0"
    log
    log USB dongles found:

    readarray -t dongles < <(ls -Alhr /dev/serial/by-id | awk '{print $11, $10, $9}')
    for i in "${dongles[@]}"
    do
      log "$i"
    done

    log
}

prepare_python () {
    # dependencies needed for https://github.com/JelmerT/cc2538-bsl
    log "Check python dependencies"
    log
    dep_array=("pyserial" "intelhex" "python-magic")
    pip_array=( $(pip list | grep -v "^Package *Version$" | grep -v "^-*$" | cut -d ' ' -f 1) )

    for dep in ${dep_array[@]}; do
       echo "${pip_array[@]}" | grep -q "$dep" &&  \
          log "Already installed $dep" || \
          pip install $dep
    done
    log
}

main $# $1 $2 $3 $4
