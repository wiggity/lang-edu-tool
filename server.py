import socket

MY_SOCK = "mysock"

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

s.bind(MY_SOCK)

s.listen(1)

conn, addr = s.accept()
print 'Connected by', addr
while 1:
	data = conn.recv(1024)
	if not data: 
		break
	print data
	conn.send(data)
conn.close()
