# reject all messages which are not of interest (return 0)

def filter_syslog_message(message=''):

    if message in 'asup.smtp.drop':              # autosupport mail was not sent for host
        return 0
    if message in 'asup.smtp.sent':              # system Notification mail sent
        return 0
    if message in 'asup.general.reminder':       # autosupport is not configured to send to NetApp
        return 0
    if message in 'asup.smtp.detailNotSent':     # no autosupport.to recipients specified
        return 0
    if message in 'cecc_log.entry:warning':      # Non Fatal Correctable DRAM ECC Channel x
        return 0
    if message in 'cifs.terminationNotice':      # cifs shut down completed, cifs terminated
        return 0
    if message in 'kern.syslogd.restarted':      # syslog daemon has been restarted due to syslog.conf changes
        return 0
    if message in 'kern.uptime.filer':           # regular update message 1x per h
        return 0
    if message in 'kern.log.rotate':             # system filer is running netApp release
        return 0
    if message in 'mgr.boot.disk_done':          # boot message
        return 0
    if message in 'nbt.nbns.registrationComplete':  # all cifs name registrations have completed for the local server
        return 0
    if message in 'raid.rg.scrub.done':          # scrub completed
        return 0
    if message in 'raid.rg.scrub.summary.cksum': # scrub found 0 checksum errors
        return 0
    if message in 'raid.rg.scrub.suspended':     # scrub suspended at stripe
        return 0
    if message in 'raid.rg.scrub.resume':        # resuming scrub at stripe
        return 0
    if message in 'raid.scrub.suspended':        # disk scrub suspended
        return 0
    if message in 'rc':                          # timed: time daemon started
        return 0
    if message in 'ses.channel.rescanInitiated': # Initiating rescan on channel
        return 0
    if message in 'sfu.firmwareUpToDate':        # firmware is up-to-date on all disk shelves
        return 0
    if message in 'wafl.scan.start':             # starting block reallocation on aggregate
        return 0
    if message in 'wafl.scan.br.realloc.done':   # block reallocation scan on aggregate
        return 0
    if message in 'wafl.scan.br.redir.done':     # redirect scan on aggregate is complete
        return 0

    return True
