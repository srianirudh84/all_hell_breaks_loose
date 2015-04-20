#!/usr/bin/python
#Author: Anirudh Srinivasan
#Apr18 2014

import sys
import readline

def  entryfor2u4n():
    #Set variables
     base_ip = raw_input("Enter the base IP: ")
     a = int(raw_input("Enter the starting octect: "))
     #b = int(raw_input("Enter the ending octect: "))
     b = int( a + 13)
     last_octect_range = range( a, b+1)
     HOST = raw_input("Enter the hostname: ")
     hostlist = ["1" ,"2", "3", "4", "c1", "c2", "c3", "c4", "i1", "i2", "i3", "i4", "v1", "v2"]
     domain = raw_input("Enter the domain: ")
     for f,b in zip(hostlist, last_octect_range):
         print "dnscmd <type DNS server ipaddress> /recordadd %s.nutanix.com %s-%s /createptr A %s.%s" %(domain, HOST, f, base_ip, b)
         
def  entryfor2u2n():
    #Set variables
     base_ip = raw_input("Enter the base IP: ")
     a = int(raw_input("Enter the starting octect: "))
     #b = int(raw_input("Enter the ending octect: "))
     b = int( a + 6)
     last_octect_range = range( a, b+1)
     HOST = raw_input("Enter the hostname: ")
     hostlist = ["1" ,"2", "c1", "c2", "i1", "i2", "v1"]
     domain = raw_input("Enter the domain: ")
     for f,b in zip(hostlist, last_octect_range):
         print "dnscmd <type DNS server ipaddress> /recordadd %s.nutanix.com %s-%s /createptr A %s.%s" %(domain, HOST, f, base_ip, b)
         
def  entryfor1un():
    #Set variables
     base_ip = raw_input("Enter the base IP: ")
     a = int(raw_input("Enter the starting octect: "))
     #b = int(raw_input("Enter the ending octect: "))
     b = int( a + 2)
     last_octect_range = range( a, b+1)
     HOST = raw_input("Enter the hostname: ")
     hostlist = ["1" , "c1",  "i1"]
     domain = raw_input("Enter the domain: ")
     for f,b in zip(hostlist, last_octect_range):
         print "dnscmd <type DNS server ipaddress> /recordadd %s.nutanix.com %s-%s /createptr A %s.%s" %(domain, HOST, f, base_ip, b)
         
def entryfornuvms():
    no_of_ips = int(raw_input("How many IPs do you need: "))
    base_ip = raw_input("Enter the base IP: ")
    a = int(raw_input("Enter the starting octect: "))
    b = int(a + (no_of_ips - 1))
    last_octect_range = range( a, b+1)
    HOST = raw_input("Enter the hostname: ")
    hostlist = range(1,no_of_ips+1)
    domain = raw_input("Enter the domain: ")
    for f,b in zip(hostlist, last_octect_range):
         print "dnscmd <type DNS server ipaddress> /recordadd %s.nutanix.com %s-%s /createptr A %s.%s" %(domain, HOST, f, base_ip, b)
    
what_node = raw_input("Is it 2u4n, 2u2n, 1un or uvms? : ")

if what_node == "2u4n":
   entryfor2u4n()
elif what_node == "2u2n":
     entryfor2u2n()
elif what_node == "1un":
     entryfor1un()
else:
     entryfornuvms()
