import os
import sys
import signal
import socket
import syslog
import datetime
import paho.mqtt.client as mqtt
from dotenv import dotenv_values
import syslog_filter as sf              # python syslog filter for filer messages
import syslog_regex as sr               # python syslog parser for filer messages
import syslog_construct_update as scu   # construct update from message response
import syslog_construct_ha as sch       # construct ha from message response

# script and pip needs to be run as root due to socket access 
# pip install paho-mqtt

# main program

# must run as root
if os.geteuid() != 0:
    print("You need to run the program with root previleges like with sudo.")
    sys.exit()

def graceful_shutdown():
    print()
    # the will_set is not sent on graceful shutdown by design
    # we need to wait until the message has been sent, else it will not appear in the broker
    publish_result = mqttclient.publish(mqtt_state_topic, payload = "offline", qos = mqtt_qos, retain = True)
    publish_result.wait_for_publish() 
    mqttclient.disconnect()
    mqttclient.loop_stop()
    s.close()
    sys.exit()

# catch ctrl-c
def signal_handler(signum, frame):
    graceful_shutdown()

def on_connect(client, userdata, flags, rc):
    # http://www.steves-internet-guide.com/mqtt-python-callbacks/
    client.publish(mqtt_state_topic, payload = "Online", qos = 0, retain = True)

def on_publish(client, userdata, mid):
    print(f"Messages published: {mid}")

def process_env():
	# get all environment variables as dictionary
	# https://pypi.org/project/python-dotenv/
	# file either predefined or as cmd line option. option ID starts with 2
	env_file = ".env"
	if len(sys.argv) > 1:
		if os.path.isfile(sys.argv[1]) == True:
			env_file = sys.argv[1]

	syslog.syslog(f'Using env file: {env_file}')

	full_config = {
		**dotenv_values(env_file),  # load env variables for mqtt
		**os.environ,               # override loaded values with environment variables if exists
	}

	# only get the mqtt_ values from the full dict
	mqtt_config = {k: v for k, v in full_config.items() if k.startswith('mqtt_')}
	return mqtt_config

signal.signal(signal.SIGINT, signal_handler)
mqtt_config = process_env()

# when sending messages to syslog, they appear in /var/log/messages

# MQTT Parameters
# when running an a container, values can be overwritten by env vars
mqtt_server = mqtt_config['mqtt_server']
mqtt_port = int(mqtt_config['mqtt_port'])
mqtt_username = mqtt_config['mqtt_username']
mqtt_password = mqtt_config['mqtt_password']
mqtt_client_id = mqtt_config['mqtt_client_id']
mqtt_ha_topic = 'homeassistant/sensor/' + mqtt_config['mqtt_topic']
mqtt_update_topic = 'syslog/sensor/' + mqtt_config['mqtt_topic']
mqtt_state_topic = 'syslog/sensor/' + mqtt_config['mqtt_topic'] + '/availability'

# MQTT qos values (http://www.steves-internet-guide.com/understanding-mqtt-qos-levels-part-1/)
# QOS 0 – Once (not guaranteed)
# QOS 1 – At Least Once (guaranteed)
# QOS 2 – Only Once (guaranteed)
mqtt_qos = 2

# Syslog Parameters
# Insert IP of server listener. 0.0.0.0 for any
server = "0.0.0.0"
port = 514
buf = 4096
addr = (server,port)

# Open Socket for syslog messages
# https://realpython.com/python-sockets/
syslog.syslog(f'Opening syslog socket: {server}:{port}')
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(addr)

if s.bind:
    syslog.syslog(f'Opened syslog socket: {server}:{port}')
else:
    syslog.syslog(f'Could not open syslog socket: {server}:{port}. Exiting')
    sys.exit()

# MQTT client
syslog.syslog(f'Opening MQTT socket: {mqtt_server}:{mqtt_port}')

mqttclient = mqtt.Client(client_id = mqtt_client_id, clean_session = True)
mqttclient.on_connect = on_connect
# mqttclient.on_publish = on_publish      # uncomment for testing purposes    
mqttclient.username_pw_set(mqtt_username, mqtt_password)
mqttclient.will_set(mqtt_state_topic, payload = "Offline", qos = 0, retain = True)

mqttclient.connect_async(mqtt_server, port=mqtt_port, keepalive=70)
mqttclient.loop_start()

if mqttclient:
    syslog.syslog(f'Opened MQTT socket: {mqtt_server}:{mqtt_port}')
else:
    syslog.syslog(f'Could not open MQTT socket: {mqtt_server}:{mqtt_port}. Exiting')
    sys.exit()

# update the home assistant auto config info
# each item needs its own publish
# name and config are arrays
# name contains the name for the config which is the full json string defining the message
name, config = sch.construct_ha_message(mqtt_config['mqtt_topic'], mqtt_state_topic, mqtt_update_topic)

for i in range(0,len(name)): 
    ha_topic_construct = mqtt_ha_topic + '/' + name[i] + '/config'
    # print(str(i) + ' ' + ha_topic_construct)
    # print(config[i])
    mqttclient.publish(ha_topic_construct, payload = config[i], qos = mqtt_qos, retain = True)

while True:
    # sudo nc -ulp 514  (read messages from command line)
    # ss -u             (show who has last sent a message)
    # data contains the message in utf-8
    # sender is a tuple with (string)IP (int)port
    # socket.gethostbyaddr(sender[0]) returns a triple ('hostname', [], ['IP'])
    data,sender = s.recvfrom(buf)
    if not data:
        syslog.syslog(f'Cant recieve data from socket {server}:{port}. Exiting')
        break
    else:
        # only continue if the message comes from filer
        if mqtt_config['mqtt_topic'] not in socket.gethostbyaddr(sender[0])[0]:
            continue

        # decode the complete message string from syslog
        msg_string = data.decode(encoding='utf-8')

        # only continue if response is important
        if not sf.filter_syslog_message(msg_string):
            continue

        # setup response from data
        response = sr.parse_syslog_message(msg_string)
        #print(response)

        update = scu.construct_update_message(response)
        # send a mqtt update message, the format is fixed
        mqttclient.publish(mqtt_update_topic, payload = update, qos = mqtt_qos, retain = True)

graceful_shutdown()
# as reminder
# https://blog.miguelgrinberg.com/post/how-to-kill-a-python-thread
