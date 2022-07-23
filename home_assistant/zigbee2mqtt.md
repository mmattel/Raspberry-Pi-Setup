# Installing the Zigbee to MQTT Gateway

## Table of Contents

   * [Installing via Docker Compose](#installing-via-docker-compose)
      * [Setup the MQTT Broker connection](#setup-the-mqtt-broker-connection)
      * [Fix USB Device Error Issues](#fix-usb-device-error-issues)
   * [Update the Zigbee USB Gateway adapter](#update-the-zigbee-usb-gateway-adapter)

<!-- Created by https://github.com/ekalinin/github-markdown-toc -->

With the [Zigbee to MQTT](https://www.zigbee2mqtt.io) bridge, you can use your Zigbee devices without the vendor's bridge or gateway. It bridges events and allows you to control your Zigbee devices via MQTT. In this way you can integrate your Zigbee devices with whatever smart home infrastructure you are using.

<p align="center">
<img src="../images/zigbee_mqtt_architecture.png" width="700" title=" Zigbee2MQTT">
</p>

Note as MQTT is used, do not install in Home Assistant the Zigbee Home Automation (ZHA) or deCONZ / Phoscon extensions. Use MQTT instead.

## Installing via Docker Compose

Note you should plugin the Zigbee USB Gateway adapter before configuring to avoid startup issues.

As tip, [Phoscon ConBee II - Universal Zigbee USB-Gateway](https://www.amazon.de/ConBee-das-universelle-Zigbee-USB-Gateway/dp/B07PZ7ZHG5/ref=sr_1_2?__mk_de_DE=ÅMÅŽÕÑ&crid=1WSYKN1A08TY1&keywords=Phoscon+ConBee+II+-+das+universelle+Zigbee+USB-Gateway&qid=1658563005&s=ce-de&sprefix=phoscon+conbee+ii+-+das+universelle+zigbee+usb-gateway%2Celectronics%2C188&sr=1-2) from _dresden electronik_ is a gateway with many positive reviews.  

To get your `serial/by-id` value, connect the device run: `ls -l /dev/serial/by-id` and see the output.

Use the directory `/home/<your-user>/docker` as base for the volume.

```
version: '3.8'
services:
  zigbee2mqtt:
    container_name: zigbee2mqtt
    image: koenkk/zigbee2mqtt
    restart: unless-stopped
    volumes:
      - /home/<your-user>/docker/zigbee2mqtt/data:/app/data
      - /run/udev:/run/udev:ro
    ports:
      # Frontend port
      - 8090:8080
    environment:
      - TZ=Europe/Berlin
    devices:
      # Do not use /dev/ttyUSBX serial devices, as those mappings can change over time.
      # Instead, use the /dev/serial/by-id/X serial device for your Zigbee stick like
      #- "/dev/serial/by-id/usb-dresden_elektronik_ingenieurtechnik_GmbH_ConBee_II_DE2478344-if00:/dev/ttyACM0"
    group_add:
      - dialout
    user: "${LOCAL_USER}:${LOCAL_GROUP}"
```

When you have started the container, it will most likely fail for some reasons:

- The connection to the MQTT broker (mosquitto) is not setup in `configuration.yaml`.
- When using the Conbee II, you have not added the `adapter: deconz` entry in `configuration.yaml`.
- You have not connected the Zigbee USB Gateway adapter or misconfigured its device definition.

See the log responses in `Dozzle` for details.

If the Zigbee USB Gateway adapter is not connected or misconfigured, you will see log messages like: `Error: Error while opening serialport 'Error: Error: No such file or directory, cannot open /dev/ttyACM0'` 

When the container is running, you can access Zigbee2MQTT via `https://<your-server/ip>:8090`.

### Setup the MQTT Broker connection

Edit the `configuration.yaml` and set the server respectively user and password if required. Note that the URL for the server is `mqtt://fqdn:1883`

`sudo vi ~/docker/zigbee2mqtt/data/configuration.yaml`

### Fix USB Device Error Issues

- Connect the Zigbee USB Gateway adapter
- When using the Conbee II, check if you need to _add_ `adapter: deconz` in [configuration.yaml](https://www.zigbee2mqtt.io/guide/adapters/#other).
- Check the `serial/by-id` value with `ls -l /dev/serial/by-id` and add it to the docker-compose file.
- Check the [Zigbee2MQTT fails to start](https://www.zigbee2mqtt.io/guide/installation/20_zigbee2mqtt-fails-to-start.html#zigbee2mqtt-fails-to-start) section.
- When all checked, restart the container.

## Update the Zigbee USB Gateway adapter

This is not possible using Zigbee2MQTT, at least I have not found a way. When using  ConBee II, it must be done in a different way. A good description can be found here: [How to update ConBee/ConBee II firmware in Windows 10](https://flemmingss.com/how-to-update-conbee-conbee-ii-firmware-in-windows-10/).
