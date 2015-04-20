#!/usr/bin/python

import commands
import readline
def get_range(start_oct, end_oct):
	base_ip = raw_input("Enter the base ip : ")
	for octet in xrange(int(start_oct), int(end_oct) + 1):
		ip = base_ip + "." + str(octet)
		status, output = commands.getstatusoutput(' ping -c 2 %s' %ip)
		if status == 0:
			print "IP %s is on the network" %ip
		elif status != 0:
			print "IP %s is not on the network" %ip

a = raw_input("Enter the starting octect: ")
b = raw_input("Enter the ending octect: ")
get_range(a, b)

