import json

 #   message[0] # timestamp "%Y.%m.%d"
 #   message[1] # timestamp "%H:%M"
 #   message[2] # type
 #   message[3] # severity
 #   message[4] # set the uptime
 #   message[5] # set the message
 #   message[6] # construct the complete message

def construct_ha_message(mqtt_topic, mqtt_availability_topic, mqtt_state_topic):

	config = ['']
	name = ['']

	# https://www.home-assistant.io/integrations/sensor.mqtt/
	# device_class: https://www.home-assistant.io/integrations/sensor/
	# "device_class": "xyz",
	# mdi:alert-octagon
	i = 0
	date = {
		"name": mqtt_topic + '/' + "Date",
		"state_topic": mqtt_state_topic,
		"value_template": "{{value_json.date}}",
		"unique_id": mqtt_topic + "_sensor_date",
		"availability_topic": mqtt_availability_topic,
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
	name[i] = 'date'
	config[i] = json.dumps(date)

	i += 1
	name.append(1)
	config.append(1)
	time = {
		"name": mqtt_topic + '/' + "Time",
		"state_topic": mqtt_state_topic,
		"value_template": "{{value_json.time}}",
		"unique_id": mqtt_topic + "_sensor_time",
		"availability_topic": mqtt_availability_topic,
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
	name[i] = 'time'
	config[i] = json.dumps(time)

	i += 1
	name.append(1)
	config.append(1)
	type = {
		"name": mqtt_topic + '/' + "Type",
		"state_topic": mqtt_state_topic,
		"value_template": "{{value_json.type}}",
		"unique_id": mqtt_topic + "_sensor_type",
		"availability_topic": mqtt_availability_topic,
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
	name[i] = 'type'
	config[i] = json.dumps(type)

	i += 1
	name.append(1)
	config.append(1)
	severity = {
		"name": mqtt_topic + '/' + "Severity",
		"state_topic": mqtt_state_topic,
		"value_template": "{{value_json.severity}}",
		"unique_id": mqtt_topic + "_sensor_severity",
		"availability_topic": mqtt_availability_topic,
		"device": {
			"identifiers": [
				mqtt_topic + "_sensor"
			],
			"name": mqtt_topic + " Sensors",
			"model": "FAS2020",
			"manufacturer": "NetApp"
		},
		#"icon_template": "{% if {{value_json.severity}} == 'warning') %} mdi:alert-octagon {% else %} mdi:alert-circle-outline {% endif %}"
		"icon": "mdi:alert-octagon-outline"
	}
	name[i] = 'severity'
	config[i] = json.dumps(severity)

#	i += 1
#	name.append(1)
#	config.append(1)
#	uptime = {
#		"name": mqtt_topic + '/' + "Uptime",
#		"state_topic": mqtt_state_topic,
#		"value_template": "{{value_json.uptime}}",
#		"unique_id": mqtt_topic + "_sensor_uptime",
#		"availability_topic": mqtt_availability_topic,
#		"device": {
#			"identifiers": [
#				mqtt_topic + "_sensor"
#			],
#			"name": mqtt_topic + " Sensors",
#			"model": "FAS2020",
#			"manufacturer": "NetApp"
#		},
#		"icon": "mdi:arrow-up-bold"
#	}
#	name[i] = 'uptime'
#	config[i] = json.dumps(uptime)

	i += 1
	name.append(1)
	config.append(1)
	message = {
		"name": mqtt_topic + '/' + "Message",
		"state_topic": mqtt_state_topic,
		"value_template": "{{value_json.message}}",
		"unique_id": mqtt_topic + "_sensor_message",
		"availability_topic": mqtt_availability_topic,
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
	name[i] = 'message'
	config[i] = json.dumps(message)

	i += 1
	name.append(1)
	config.append(1)
	full = {
		"name": mqtt_topic + '/' + "Full Message",
		"state_topic": mqtt_state_topic,
		"value_template": "{{value_json.full}}",
		"unique_id": mqtt_topic + "_sensor_full",
		"availability_topic": mqtt_availability_topic,
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
	name[i] = 'full'
	config[i] = json.dumps(full)

	return name, config
