 #   message[0] # timestamp "%Y.%m.%d"
 #   message[1] # timestamp "%H:%M"
 #   message[2] # short
 #   message[3] # severity
 #   message[4] # set the uptime
 #   message[5] # set the message

# reject all messages wich are not of interest
def filter_syslog_message(message=''):

    if message[1] == 'kern.uptime.filer':
        return 0
    if message[1] == 'asup.general.reminder':
        return 0
    if message[1] == 'kern.syslogd.restarted':
        return 0
    if message[1] == 'asup.smtp.detailNotSent':
        return 0

    return True
