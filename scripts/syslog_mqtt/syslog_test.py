import socket

# script and pip needs to be run as root due to access to socket
# pip install paho-mqtt

#message = '<30>Jan 19 17:00:00 [kern.uptime.filer:info]:   5:00pm up  4 days,  5:39 241578229 NFS ops, 4430 CIFS ops, 0 HTTP ops, 0 FCP ops, 0 iSCSI ops'
message = '<29>Jan 15 20:25:12 [asup.smtp.sent:notice]: System Notification mail sent: System Notification from filer (USER_TRIGGERED (do)) INFO'

host = "127.0.0.1"
port = 514

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((host,port))
s.send(message.encode(encoding='utf-8'))
