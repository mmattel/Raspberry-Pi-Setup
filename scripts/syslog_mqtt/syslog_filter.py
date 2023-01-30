#   message[0] # timestamp "%Y.%m.%d"
#   message[1] # timestamp "%H:%M"
#   message[2] # type
#   message[3] # severity
#   message[4] # set the uptime
#   message[5] # set the message
#   message[6] # set the full message

# reject all messages which are not of interest (return 0)
def filter_syslog_message(message=''):

    if message[2] == 'asup.smtp.drop':              # autosupport mail was not sent for host
        return 0
    if message[2] == 'asup.smtp.sent':              # system Notification mail sent
        return 0
    if message[2] == 'asup.general.reminder':       # autosupport is not configured to send to NetApp
        return 0
    if message[2] == 'asup.smtp.detailNotSent':     # no autosupport.to recipients specified
        return 0
    if message[2] == 'cifs.terminationNotice':      # cifs shut down completed, cifs terminated
        return 0
    if message[2] == 'kern.syslogd.restarted':      # syslog daemon has been restarted due to syslog.conf changes
        return 0
    if message[2] == 'kern.uptime.filer':           # regular update message 1x per h
        return 0
    if message[2] == 'kern.log.rotate':             # system filer is running netApp release
        return 0
    if message[2] == 'mgr.boot.disk_done':          # boot message
        return 0
    if message[2] == 'nbt.nbns.registrationComplete':  # all cifs name registrations have completed for the local server
        return 0
    if message[2] == 'raid.rg.scrub.done':          # scrub completed
        return 0
    if message[2] == 'raid.rg.scrub.summary.cksum': # scrub found 0 checksum errors
        return 0
    if message[2] == 'raid.rg.scrub.suspended':     # scrub suspended at stripe
        return 0
    if message[2] == 'raid.rg.scrub.resume':        # resuming scrub at stripe
        return 0
    if message[2] == 'raid.scrub.suspended':        # disk scrub suspended
        return 0
    if message[2] == 'rc':                          # timed: time daemon started
        return 0
    if message[2] == 'ses.channel.rescanInitiated': # Initiating rescan on channel
        return 0
    if message[2] == 'sfu.firmwareUpToDate':        # firmware is up-to-date on all disk shelves
        return 0
    if message[2] == 'wafl.scan.start':             # starting block reallocation on aggregate
        return 0
    if message[2] == 'wafl.scan.br.realloc.done':   # block reallocation scan on aggregate
        return 0
    if message[2] == 'wafl.scan.br.redir.done':     # redirect scan on aggregate is complete
        return 0

    return True
