# Mosquitto MQTT broker

[Mosquitto](https://mosquitto.org) is an open source message broker that implements the MQTT protocol.

The MQTT protocol provides a lightweight method of carrying out messaging using a publish/subscribe model. This makes it suitable for Internet of Things messaging such as with low power sensors or mobile devices such as phones, embedded computers or microcontrollers.

<p align="center">
<img src="../images/MosquittoMQTTArchitecture.png" width="450" title=" Mosquitto MQTT broker">
</p>

The Mosquitto MQTT broker is the central hub for messages. The the [Z-Wave to MQTT Gateway](./zwavejs2mqtt.md) and [Home Assistant](./ha_install.md) will connect to it.
