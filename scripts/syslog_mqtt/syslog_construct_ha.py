import json

 #   message[0] # timestamp "%Y.%m.%d"
 #   message[1] # timestamp "%H:%M"
 #   message[2] # type
 #   message[3] # severity
 #   message[4] # set the uptime
 #   message[5] # set the message

def construct_ha_message(mqtt_topic, mqtt_state_topic, mqtt_update_topic):

    config = [''] * 6
    name = [''] * 6

    # https://www.home-assistant.io/integrations/sensor.mqtt/
    # device_class: https://www.home-assistant.io/integrations/sensor/
    # "device_class": "xyz",
    date = {
        "name": mqtt_topic + '/' + "Date",
        "state_topic": mqtt_update_topic,
        "value_template": "{{value_json.date}}",
        "unique_id": mqtt_topic + "_sensor_date",
        "availability_topic": mqtt_state_topic,
        "device": {
            "identifiers": [
                mqtt_topic + "_sensor"
            ],
            "name": mqtt_topic + " Sensors",
            "model": "FAS2020",
            "manufacturer": "NetApp"
        },
        "icon": "mdi:calendar"
    }
    name[0] = 'date'
    config[0] = json.dumps(date)

    time = {
        "name": mqtt_topic + '/' + "Time",
        "state_topic": mqtt_update_topic,
        "value_template": "{{value_json.time}}",
        "unique_id": mqtt_topic + "_sensor_time",
        "availability_topic": mqtt_state_topic,
        "device": {
            "identifiers": [
                mqtt_topic + "_sensor"
            ],
            "name": mqtt_topic + " Sensors",
            "model": "FAS2020",
            "manufacturer": "NetApp"
        },
        "icon": "mdi:clock-outline"
    }
    name[1] = 'time'
    config[1] = json.dumps(time)

    type = {
        "name": mqtt_topic + '/' + "Type",
        "state_topic": mqtt_update_topic,
        "value_template": "{{value_json.type}}",
        "unique_id": mqtt_topic + "_sensor_type",
        "availability_topic": mqtt_state_topic,
        "device": {
            "identifiers": [
                mqtt_topic + "_sensor"
            ],
            "name": mqtt_topic + " Sensors",
            "model": "FAS2020",
            "manufacturer": "NetApp"
        },
        "icon": "mdi:information-outline"
    }
    name[2] = 'type'
    config[2] = json.dumps(type)

    severity = {
        "name": mqtt_topic + '/' + "Severity",
        "state_topic": mqtt_update_topic,
        "value_template": "{{value_json.severity}}",
        "unique_id": mqtt_topic + "_sensor_severity",
        "availability_topic": mqtt_state_topic,
        "device": {
            "identifiers": [
                mqtt_topic + "_sensor"
            ],
            "name": mqtt_topic + " Sensors",
            "model": "FAS2020",
            "manufacturer": "NetApp"
        },
        "icon": "mdi:alert-circle-outline"
    }
    name[3] = 'severity'
    config[3] = json.dumps(severity)

    uptime = {
        "name": mqtt_topic + '/' + "Uptime",
        "state_topic": mqtt_update_topic,
        "value_template": "{{value_json.uptime}}",
        "unique_id": mqtt_topic + "_sensor_uptime",
        "availability_topic": mqtt_state_topic,
        "device": {
            "identifiers": [
                mqtt_topic + "_sensor"
            ],
            "name": mqtt_topic + " Sensors",
            "model": "FAS2020",
            "manufacturer": "NetApp"
        },
        "icon": "mdi:arrow-up-bold"
    }
    name[4] = 'uptime'
    config[4] = json.dumps(uptime)

    message = {
        "name": mqtt_topic + '/' + "Message",
        "state_topic": mqtt_update_topic,
        "value_template": "{{value_json.message}}",
        "unique_id": mqtt_topic + "_sensor_message",
        "availability_topic": mqtt_state_topic,
        "device": {
            "identifiers": [
                mqtt_topic + "_sensor"
            ],
            "name": mqtt_topic + " Sensors",
            "model": "FAS2020",
            "manufacturer": "NetApp"
        },
        "icon": "mdi:file-document-outline"
    }
    name[5] = 'message'
    config[5] = json.dumps(message)

    return name, config
