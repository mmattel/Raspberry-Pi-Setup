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

def graceful_shutdown():
    print()
    mqttclient.disconnect()
    mqttclient.loop_stop()
    s.close()
    sys.exit()

# catch ctrl-c
#def signal_handler(signal, frame):
#    graceful_shutdown()
#
#signal.signal(signal.SIGINT, signal_handler)

# get all environment variables as dictionary
# https://pypi.org/project/python-dotenv/
# pip install python-dotenv (if necessary)
full_config = {
    **dotenv_values(".env"),    # load .env variables for mqtt
    **os.environ,               # override loaded values with environment variables if exists
}

# only get the mqtt_ values from the full dict
mqtt_config = {k: v for k, v in full_config.items() if k.startswith('mqtt_')}

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

def on_connect(client, userdata, flags, rc):
    # http://www.steves-internet-guide.com/mqtt-python-callbacks/
    client.publish(mqtt_state_topic, payload = "Online", qos = 0, retain = True)

mqttclient = mqtt.Client(client_id = mqtt_client_id, clean_session = True)
mqttclient.on_connect = on_connect
mqttclient.username_pw_set(mqtt_username, mqtt_password)
mqttclient.will_set(mqtt_state_topic, payload = "Offline", qos = 0, retain = True)

mqttclient.connect_async(mqtt_server, port=mqtt_port, keepalive=70)
mqttclient.loop_start()

if mqttclient:
    syslog.syslog(f'Opened MQTT socket: {mqtt_server}:{mqtt_port}')
else:
    syslog.syslog(f'Could not open MQTT socket: {mqtt_server}:{mqtt_port}. Exiting')
    sys.exit()

# response = sr.parse_syslog_message(message)
# json = scu.construct_json_message(response)
# sys.exit()

while True:
    # sudo nc -ulp 514  (read messages from command line)
    # ss -u             (show who has last sent a message)
    # data contains the message in utf-8
    # sender is a tuple with (string)IP (int)port
    # socket.gethostbyaddr(sender[0]) returns a triple ('hostname', [], ['IP'])
    data,sender = s.recvfrom(buf)
    if not data:
        message = f'Cant revieve data from socket {server}:{port}. Exiting'
        print (message, file=log_file, flush=True)
        break
    else:
        # only continue if the message comes from filer
        if "filer" not in socket.gethostbyaddr(sender[0])[0]:
            continue
        # setup response from data
        response = sr.parse_syslog_message(data.decode(encoding='utf-8'))
        # only continue if response is important
        if not sf.filter_syslog_message(response):
            continue
        print(response)
        update = scu.construct_update_message(response)
        # send a filer update message, the format is fixed
        mqttclient.publish(mqtt_update_topic, payload = update, qos = 0, retain = True)

graceful_shutdown()
# as reminder
# https://blog.miguelgrinberg.com/post/how-to-kill-a-python-thread
