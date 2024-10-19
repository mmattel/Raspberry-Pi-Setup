import json

#   message[0] # timestamp "%Y.%m.%d"
#   message[1] # timestamp "%H:%M"
#   message[2] # type
#   message[3] # severity
#   message[4] # set the uptime
#   message[5] # set the message
#   message[6] # set the full message

def construct_update_message(message):

	construct = {
		'date': message[0],
		'time': message[1],
		'type': message[2],
		'severity': message[3],
		'uptime': message[4],
		'message': message[5],
		'full': message[6],
	}

	final = json.dumps(construct)

	# print(json.dumps(construct, indent=4))

	return final
