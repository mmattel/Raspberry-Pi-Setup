# reject all messages which are not of interest (return False)

def filter_syslog_message(message=''):

	matches = [
		'asup.smtp.drop',                 # autosupport mail was not sent for host
		'asup.smtp.sent',                 # system Notification mail sent
		'asup.general.reminder',          # autosupport is not configured to send to NetApp
		'asup.smtp.detailNotSent',        # no autosupport.to recipients specified
		'cecc_log.entry:warning',         # Non Fatal Correctable DRAM ECC Channel x
		'cifs.terminationNotice',         # cifs shut down completed, cifs terminated
		'kern.log.rotate',                # system filer is running netApp release
		'kern.syslogd.restarted',         # syslog daemon has been restarted due to syslog.conf changes
		'kern.uptime.filer',              # regular update message 1x per h
		'mgr.boot.disk_done',             # boot message
		'nbt.nbns.registrationComplete',  # all cifs name registrations have completed for the local server
		'raid.rg.scrub.done',             # scrub completed
		'raid.rg.scrub.resume',           # resuming scrub at stripe
		#'raid.rg.scrub.summary.cksum',    # scrub found 0 checksum errors
		'raid.rg.scrub.suspended',        # scrub suspended at stripe
		'raid.scrub.suspended',           # disk scrub suspended
		'rc',                             # timed: time daemon started
		'ses.channel.rescanInitiated',    # Initiating rescan on channel
		'sfu.firmwareUpToDate',           # firmware is up-to-date on all disk shelves
		'wafl.scan.br.realloc.done',      # block reallocation scan on aggregate
		'wafl.scan.br.redir.done',        # redirect scan on aggregate is complete
		'wafl.scan.start',                # starting block reallocation on aggregate
		'last message repeated'           # this message is a string and has no valid timestamp etc
	]

	# not important stuff
	# check for any occurrence array elements in the message
	if any(x in message for x in matches):
		return False

	# anything else is important
	return True
