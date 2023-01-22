#   message[0] # timestamp "%Y.%m.%d"
#   message[1] # timestamp "%H:%M"
#   message[2] # short
#   message[3] # severity
#   message[4] # set the uptime
#   message[5] # set the message

# reject all messages which are not of interest (return 0)
def filter_syslog_message(message=''):

    if message[2] == 'kern.uptime.filer':       # regular update message 1x per h
        return 0
    if message[2] == 'asup.smtp.drop':          # autosupport mail was not sent for host
        return 0
    if message[2] == 'asup.general.reminder':   # autosupport is not configured to send to NetApp
        return 0
    if message[2] == 'kern.syslogd.restarted':  # syslog daemon has been restarted due to syslog.conf changes
        return 0
    if message[2] == 'asup.smtp.detailNotSent': # no autosupport.to recipients specified
        return 0

    return True
