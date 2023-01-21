 #   message[0] # timestamp "%Y.%m.%d"
 #   message[1] # timestamp "%H:%M"
 #   message[2] # short
 #   message[3] # severity
 #   message[4] # set the uptime
 #   message[5] # set the message

# reject all messages which are not of interest (return 0)
def filter_syslog_message(message=''):

    if message[2] == 'kern.uptime.filer':
        return 0
    if message[2] == 'asup.general.reminder':
        return 0
    if message[2] == 'kern.syslogd.restarted':
        return 0
    if message[2] == 'asup.smtp.detailNotSent':
        return 0

    return True
