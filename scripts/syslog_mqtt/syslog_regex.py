import re
import datetime
import syslog

#   message[0] # timestamp "%Y.%m.%d"
#   message[1] # timestamp "%H:%M"
#   message[2] # type
#   message[3] # severity
#   message[4] # set the uptime
#   message[5] # set the message
#   message[6] # set the full message

def parse_syslog_message(message):

	#message = '<30>Jan 19 17:00:00 [kern.uptime.filer:info]:   5:00pm up  4 days,  5:39 241578229 NFS ops, 4430 CIFS ops, 0 HTTP ops, 0 FCP ops, 0 iSCSI ops'
	#message = '<29>Jan 15 20:25:12 [asup.smtp.sent:notice]: System Notification mail sent: System Notification from filer (USER_TRIGGERED (do)) INFO'

	# the regex creates groups based on ontap 7 standard syslog messages
	the_regex = r'<.+>(.+?(?=.\[))..(.+?(?=.\:).).(.*?)(\]:\s+)(\D)?(?(5)(.*$)|.+(up)(\s*)(.+?(?=,))(.+?(?=:).\d*.)(.*))'

	target = [''] * 12			  # initaialize array with 12 empty elements 
	final = [''] * 8				# final array contains all info at the right locations

	m = re.search(the_regex, message)

	if m:
		if m.group(0) is not None:
			target[0] = m.group(0)		# full message
		if m.group(1) is not None:
			target[1] = m.group(1)		# timestamp
		if m.group(2) is not None:
			target[2] = m.group(2)		# short
		if m.group(3) is not None:
			target[3] = m.group(3)		# severity 
		if m.group(4) is not None:
			target[4] = m.group(4)		# not of interest
		if m.group(5) is not None:
			target[5] = m.group(5)		# if 7 is empty, message = 5+6
		if m.group(6) is not None:
			target[6] = m.group(6)		# if 7 is empty, message = 5+6
		if m.group(7) is not None:
			target[7] = m.group(7)		# empty or the word 'up'
		if m.group(8) is not None:
			target[8] = m.group(8)		# not of interest
		if m.group(9) is not None:
			target[9] = m.group(9)		# number of days (5 days)
		if m.group(10) is not None:
			target[10] = m.group(10)	# not of interest
		if m.group(11) is not None:
			target[11] = m.group(11)	# final message

	# add year --> 2023 Jan 19 17:00:00
	target[1] = str(datetime.datetime.now().year) + ' ' + target[1]

	# there can be cases that strptime fails and would kill the program
	# but the string causing the issue is not printed therefore using try/except
	try:
		t = datetime.datetime.strptime(target[1], "%Y %b %d %H:%M:%S")
		final[1] = t.strftime("%Y.%m.%d")	# timestamp "%Y.%m.%d"
		final[2] = t.strftime("%H:%M")		# timestamp "%H:%M"
	except:
		t = target[1]
		syslog.syslog(f'Unidentifyable time string: {t}')  # log the failed string for further investigation
		final[1] = t						# raw timestamp in case of an error
		final[2] = ""						# keep empty
		if len(target[11]) == 0:			# if the message is empty
			t = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
			target[11] = (f'Syslog Parse Error at: {t}') # prefill it with an error and timestamp

	# print for testing
	# for i in range(1, len(target)):
	#	print(i, target[i])

	final[3] = target[2]					# short
	final[4] = target[3]					# severity

	if len(target[7]) == 0:
		final[6] = target[5] + target[6]	# set the message
	else:
		final[5] = target[9]				# set the uptime 
		final[6] = target[11]				# set the message

	# construct a full message based on the regex outcome
	# special care on the uptime as it can be empty, avoid double whitespace
	ut = final[5] + ' '
	if ut.isspace():
		ut = ''
	final[7] = final[1] + ' ' + final[2] + ' ' + final[3] + ' ' + final[4] + ' ' +  ut + final[6]

	# remove the first entry (full message) as not necessary
	final = final[1:]

	# print for testing
	# for i in range(1, len(final)):
	#	print(i, final[i])

	return final
