# Installing the Z-Wave to MQTT Gateway

A fully configurable [Z-Wave to MQTT Gateway](https://zwave-js.github.io/zwavejs2mqtt/#/) and Control Panel  when you want to build a Z-Wave hub. This is necessary for the official Home Assistant integration when you use a Z-Wave USB dongle that acts as central point. 

zwavejs2mqtt exposes Z-Wave devices to an MQTT broker (to be installed, [Mosquitto MQTT](https://mosquitto.org)) in a fully configurable manner.

See the [installation](https://zwave-js.github.io/zwavejs2mqtt/#/getting-started/docker?id=installation) for options.

## Installing via Docker Compose

Use the [Run as a Service](https://zwave-js.github.io/zwavejs2mqtt/#/getting-started/docker?id=run-as-a-service) info for the docker compose file, adopt according your environment.

To get your `serial/by-id` value, connect the device run: `ls -l /dev/serial/by-id` and see the output.

Note that if you get `No such file or directory` but there is an output when using `by-path` instead of `by-id`, check with `dmesg -wH` if you get a response from connecting the device. If that works, you may have run into a [debian bug](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1035094). To solve this issue, make a copy of the original file `/lib/udev/rules.d/60-serial.rules` and create a new one using the content of the solution referenced in the bug report. Finally reboot and `ls -l /dev/serial/by-id` should run fine.

Use the directory `/home/<your-user>/docker` as base for the volume.

```
version: "3.7"
services:
  zwavejs2mqtt:
    container_name: zwavejs2mqtt
    image: zwavejs/zwavejs2mqtt:latest
    restart: always
    logging:
      driver: "json-file"
      options:
        max-size: "200k"
        max-file: "10"
    tty: true
    stop_signal: SIGINT
    environment:
      - SESSION_SECRET=mysupersecretkey
      - ZWAVEJS_EXTERNAL_CONFIG=/usr/src/app/store/.config-db
      # Uncomment if you want log times and dates to match your timezone instead of UTC
      # Available at https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
      #- TZ=America/New_York
    networks:
      - zwave
    devices:
      # Do not use /dev/ttyUSBX serial devices, as those mappings can change over time.
      # Instead, use the /dev/serial/by-id/X serial device for your Z-Wave stick like
      #- "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A10M1RS0-if00-port0:/dev/zwave"
      - "/dev/serial/by-id/insert_stick_reference_here:/dev/zwave"
    volumes:
      - zwave-config:/usr/src/app/store
      # Or by using local folder
      #- /home/<your-user>/docker/zwave-config:/usr/src/app/store
    ports:
      - "8091:8091" # port for web interface
      - "3000:3000" # port for Z-Wave JS websocket server
    # user: "${LOCAL_USER}:${LOCAL_GROUP}"
networks:
  zwave:
volumes:
  zwave-config:
    name: zwave-config
```

Note the [SESSION_SECRET](https://zwave-js.github.io/zwavejs2mqtt/#/guide/env-vars?id=environment-variables) is used by the [express.js](https://github.com/expressjs/session#secret) library in the container, necessary to sign the session ID cookie and will reduce the ability to hijack a session. This is less critical if this container is not accessible outsite your network. If not provided, a default one is used.

More environment variables can be provided, see the [list](https://zwave-js.github.io/zwavejs2mqtt/#/guide/env-vars?id=environment-variables) for details.

When the container is running, you can access zwavejs2mqtt via `http://<your-server/ip>:8091`

If you have enabled authentication and forgot the password, the default username is `admin`, password is `zwave`.

If you previously have added MQTT Explorer, you see post configuring that zwave has been added and messages are posted.  
