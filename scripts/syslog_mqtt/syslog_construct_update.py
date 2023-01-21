import json

 #   message[0] # timestamp "%Y.%m.%d"
 #   message[1] # timestamp "%H:%M"
 #   message[2] # short
 #   message[3] # severity
 #   message[4] # set the uptime
 #   message[5] # set the message
 
def construct_update_message(message=''):

    construct = {
        'date': message[0],
        'time': message[1],
        'host': message[2],
        'severity': message[3],
        'uptime': message[4],
        'message': message[5],
    }

    final = json.dumps(construct)

    # print(json.dumps(construct, indent=4))

    return final
