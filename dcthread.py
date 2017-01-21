import os
import socket
import sys
import subprocess
import threading
import time

class DispCaptureThread(object):
	def __init__(self, user, host, port, timeout):
		self.user = user
		self.host = host
		self.port = port
		self.duration = duration

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((self.get_ip(), port))

	def get_ip(self):
		return os.popen('/sbin/ifconfig eth0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1').read()

	def listen(self):
		self.sock.listen(1)
		while True:
			conn, addr = self.sock.accept()
			print ("Connected from " + str(addr))
			threading.Thread(target = self.recv_thread,args = (conn,addr)).start()

	def recv_thread(self, conn, addr):
		while True:
			data = conn.recv(32).decode()

			if data == "capture:hdmi":
				print "Start capturing HDMI during" + self.duration + " seconds"
				self.start_timer()
				self.capture_hdmi()

			time.sleep(1)

		conn.close()

	def start_timer(self):
		timeout = self.duration + 5
		threading.Timer(timeout, self.timer_expired).start()

	def timer_expired(self):
		dest = self.user + "@" + self.host + ":/home/" + self.user + "/output/"
		self._exec("scp demo.mp4 " + dest)

	def capture_hdmi(self):
		self._exec("python picapture.py -t " + str(self.duration*1000))

	def _exec(self, args):
		out = args.split(' ')
		subprocess.Popen(out)

def help():
	print """
	Available options

	-u	username.
	-s	DIVA server hostname or ip.
	-p	port number.
	-t	duration time for display capture. (unit is seconds)

	Example: python dcthread.py -u diva -s diva-server -p 3506 -t 120
	""";

if __name__ == '__main__':
	options = sys.argv

	# Default values
	user = 'diva'
	host = 'diva-server'
	port = 3506
	duration = 120	#unit is seconds

	# Help - not host ;)
	if '-h' in options:
		help()
		exit()

	if '-u' in options:
		index = options.index('-u') + 1
		user = options[index]

	if '-s' in options:
		index = options.index('-s') + 1
		host = options[index]

	if '-p' in options:
		index = options.index('-p') + 1
		port = int(options[index])

	if '-t' in options:
		index = options.index('-t') + 1
		duration = int(options[index])

	DispCaptureThread(user, host, port, duration).listen()
