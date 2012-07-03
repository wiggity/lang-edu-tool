#!/usr/bin/python

import socket, sys

def main(args) :
	if len(args) == 1 :
		# Assume INET sockets

		start_ip_sock()

	else :
		# Use unix sockets
		start_ux_sock()


def start_ux_sock() :
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


def start_ip_sock() :
	SOCK_ADDR = "localhost"
	SOCK_PORT = 12345

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((SOCK_ADDR, SOCK_PORT))

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

if __name__ == "__main__" :
	main(sys.argv)
