import json

 #   message[0] # timestamp "%Y.%m.%d"
 #   message[1] # timestamp "%H:%M"
 #   message[2] # short
 #   message[3] # severity
 #   message[4] # set the uptime
 #   message[5] # set the message

def construct_ha_message(message=''):

    construct = {
        'date':
                {'name': 'Date',
                 'icon': 'calendar',
                 'sensor_type': 'sensor',
                 'value_template': message[1]},
        'time':
                {'name': 'Time',
                 'icon': 'calendar-clock',
                 'sensor_type': 'sensor',
                 'value_template': message[2]},
        'host':
                {'name': 'Host',
                 'icon': 'server',
                 'sensor_type': 'sensor',
                 'value_template': message[3]},
        'severity':
                {'name': 'Severity',
                 'icon': 'alert-circle',
                 'sensor_type': 'sensor',
                 'value_template': message[4]},
        'uptime':
                {'name': 'Up Time',
                 'icon': 'arrow-up-bold',
                 'sensor_type': 'sensor',
                 'value_template': message[5]},
        'message':
                {'name': 'Message',
                 'icon': 'file-document-outline',
                 'sensor_type': 'sensor',
                 'value_template': message[6]},
    }

    final = json.dumps(construct)

    # print(json.dumps(construct, indent=4))

    return final
