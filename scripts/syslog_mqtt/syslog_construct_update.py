import json

 #   message[0] # timestamp "%Y.%m.%d"
 #   message[1] # timestamp "%H:%M"
 #   message[2] # short
 #   message[3] # severity
 #   message[4] # set the uptime
 #   message[5] # set the message
 
def construct_update_message(message=''):

    construct = {
        'date': message[1],
        'time': message[2],
        'host': message[3],
        'severity': message[4],
        'uptime': message[5],
        'message': message[6],
    }

    final = json.dumps(construct)

    # print(json.dumps(construct, indent=4))

    return final
