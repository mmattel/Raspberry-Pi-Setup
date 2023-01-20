import json

def construct_json_message(message=''):

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
