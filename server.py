#!/usr/bin/python

import socket, sys, signal
import threading
import SocketServer

dict_file = "dictionary.csv"

def main(args) :

	# Set the signal handler and a 5-second alarm
	signal.signal(signal.SIGINT, handler)

	IP_ADDR = "localhost"
	IP_PORT = 0

	if len(args) >= 2 :
		IP_PORT = int(args[1])

	server = ThreadedTCPServer((IP_ADDR, IP_PORT), ThreadedTCPRequestHandler)
	ip, port = server.server_address

	# Start a thread with the server -- that thread will then start one
	# more thread for each request
	server_thread = threading.Thread(target=server.serve_forever)
	# Exit the server thread when the main thread terminates
	server_thread.setDaemon(True)
	server_thread.start()
	print "Server loop running in thread: %s (%s:%i)" % (server_thread.getName(), ip, port)

	signal.pause()
	server.shutdown()

def handler(signum, frame):
	print 'Ctrl-C caught. Server shutdown called.'

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

	words = {}

	def setup(self):
		print "setup has been called..."
		# Populate memory dictionary
		f = open(dict_file, "r")

		for line in f :
			line = line.split(",")
			self.words[line[0].strip()] = line[1].strip()

	def finish(self) :
		print "finish has been called..."
		f = open(dict_file, "w")

		for k, v in self.words.iteritems() :
			f.write("%s, %s\n" % (k, v))

	def handle(self):
		while 1 :
			self.request.send("Word list in memory...\n")
			for k,v in self.words.iteritems() :
				self.request.send("%s - %s\n" % (k.ljust(15), v))
			self.request.send("...\n")
			self.request.send("Enter an option.\n1 to add a new word.\n2 to delete a word.\n3 to redisplay words.\nq to quit.\n")
			data = self.request.recv(1024).strip()

			if not data or data == 'q' :
				break

			elif data == '1' :
				self.request.send("Enter word to be added...: ")
				new_word = self.request.recv(1024).strip()
				if new_word in self.words :
					self.request.send("ERROR!\nThis word already exists. Delete it first.\n\n")
					continue
				self.request.send("Enter definition...: ")
				new_def = self.request.recv(1024).strip()
				self.words[new_word] = new_def

			elif data == '2' :
				self.request.send("Enter word to be deleted...: ")
				del_word = self.request.recv(1024).strip()
				if del_word not in self.words :
					self.request.send("ERROR!\nThis word does not exist. Thus it cannot be deleted.\n\n")
					continue
				del self.words[del_word]
		
			elif data == '3' :
				continue



class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass
if __name__ == "__main__" :
	main(sys.argv)
