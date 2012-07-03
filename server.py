#!/usr/bin/python

import socket, sys

def main(args) :

	IP_ADDR = "localhost"
	IP_PORT = 12345

	UX_SOCK = "mysock"

	if len(args) == 1 :
		# Assume INET sockets
		start_ip_sock(IP_ADDR, IP_PORT)

	else :
		if args[1] == "ipv4" or args[1] == "ip" :
			if len(args) == 3 :
				IP_PORT = int(args[2])
			start_ip_sock(IP_ADDR, IP_PORT)

		else :
			# Use unix sockets
			if len(args) == 3:
				UX_SOCK = args[2]
			start_ux_sock(UX_SOCK)


def start_ux_sock(ux_sock) :
	s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

	s.bind(ux_sock)

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


def start_ip_sock(addr, port) :

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((addr, port))

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
