#!/usr/bin/env python
#
# Copyright (c) 2013 Nutanix Inc. All rights reserved.
#Author : Anirudh Srinivasan
#26Nov2013 : dta - Modified script to run remote SSH commands 

import commands
import re
import socket
from time import time
import sys

HOST = sys.argv[1]

#Check to make sure the name actually resolves:
try:
    host = socket.gethostbyname(HOST)
except socket.gaierror, err:
    print "%s: cannot resolve hostname" % HOST, err
    sys.exit()

#Set Variables
CARBON_SERVER = '10.3.1.109'
CARBON_PORT = 2003
SSHCOMMAND = '/usr/bin/ssh -o ConnectTimeout=20 -o StrictHostKeyChecking=no'

#Check for connection
COMMAND = '%s %s /home/nutanix/prism/cli/ncli cluster version' % (SSHCOMMAND, HOST)
status,output = commands.getstatusoutput(COMMAND)
#print "STATUS: %s" % status
#print "OUTPUT: %s" % output
if status !=0:
    print "%s: \"%s\" \nUnable to pull ncli data... exiting." %(HOST,output)
    sys.exit()
#print "%s VERSION: %s" % (HOST, str(output))

#Determine the Hypervisor IP address:
COMMAND = '%s %s /home/nutanix/prism/cli/ncli host list |egrep -w "Management Server" |awk -F: \'{print $2}\'' % (SSHCOMMAND, HOST)
status,output = commands.getstatusoutput(COMMAND)
correct_ip = output.split()
host_ip_list = list(correct_ip)
#print "The host ip list is %s" %host_ip_list

# Determine the host id
# NCLI password may vary accordingly
COMMAND = '%s %s /home/nutanix/prism/cli/ncli host list |egrep -w "ID" |awk -F: \'{print $2}\'' % (SSHCOMMAND, HOST)
status,output = commands.getstatusoutput(COMMAND)
correct_output = output.split()
host_id_list = list(correct_output)
#print "The host id list is %s" %host_id_list

#Constructing a dictionary using host_ip_list and host_id_list
ip_id_dict = dict(zip(host_ip_list, host_id_list))
#print "The master dict is %s" %ip_id_dict

sock = socket.socket()
sock.connect( (CARBON_SERVER,CARBON_PORT) )

#def point_in_time_value(arg):
#        list = []
#        for key,value in ip_id_dict.iteritems():
#                ip = re.sub(r'\.','_',key)
#                HOST_REFMT = re.sub(r'-c1','',HOST)
#                x = ("%s.%s.%s" %(HOST_REFMT,ip,arg))
#                COMMAND = '%s %s /home/nutanix/bin/query_stats.sh --type=host_perf --id=%s | egrep -w %s |awk -F: \'{print $2}\'' % (SSHCOMMAND, HOST, value,arg)
#                status,output=commands.getstatusoutput(COMMAND)
#                EPOCH = int(time())
#                val = x + ' ' +str(output)+ ' ' +str(EPOCH)
#                list.append(val)
#        message = '\n'.join(list) + '\n'
#        print message
#        sock.sendall(message)

#metrics = ['CPU', 'Memory', 'Network', 'IOPS']

#for arg in metrics:
#        point_in_time_value(arg)

cpu_list = []
for key,value in ip_id_dict.iteritems():
    ip = re.sub(r'\.','_',key)
    HOST_REFMT = re.sub(r'-c1','',HOST)
    x = ("%s.%s.cpu" %(HOST_REFMT,ip))
    COMMAND = '%s %s /home/nutanix/bin/query_stats.sh --type=host_perf --id=%s | egrep -w CPU |awk -F: \'{print $2}\'' % (SSHCOMMAND, HOST, value)
    status,output=commands.getstatusoutput(COMMAND)
    #output = format((float(output)), '.2f')
    EPOCH = int(time())
    val = x + ' ' +str(output)+ ' ' +str(EPOCH)
    cpu_list.append(val)
cpu_message = '\n'.join(cpu_list) + '\n'
sock.sendall(cpu_message)
print cpu_message

mem_list = []
for key,value in ip_id_dict.iteritems():
    ip = re.sub(r'\.','_',key)
    HOST_REFMT = re.sub(r'-c1','',HOST)
    x = ("%s.%s.mem" %(HOST_REFMT,ip))
    COMMAND = '%s %s /home/nutanix/bin/query_stats.sh --type=host_perf --id=%s | egrep -w Memory |awk -F: \'{print $2}\'' % (SSHCOMMAND, HOST, value)
    status,output=commands.getstatusoutput(COMMAND)
    EPOCH = int(time())
    val = x + ' ' +str(output)+ ' ' +str(EPOCH)
    mem_list.append(val)
mem_message = '\n'.join(mem_list) + '\n'
sock.sendall(mem_message)
print mem_message

net_list = []
for key,value in ip_id_dict.iteritems():
    ip = re.sub(r'\.','_',key)
    HOST_REFMT = re.sub(r'-c1','',HOST)
    x = ("%s.%s.net" %(HOST_REFMT,ip))
    COMMAND = '%s %s /home/nutanix/bin/query_stats.sh --type=host_perf --id=%s | egrep -w Network |awk -F: \'{print $2}\'' % (SSHCOMMAND, HOST, value)
    status,output=commands.getstatusoutput(COMMAND)
    EPOCH = int(time())
    val = x + ' ' +str(output)+ ' ' +str(EPOCH)
    net_list.append(val)
net_message = '\n'.join(net_list) + '\n'
sock.sendall(net_message)
print net_message

iops_list = []
for key,value in ip_id_dict.iteritems():
    HOST_REFMT = re.sub(r'-c1','',HOST)
    ip = re.sub(r'\.','_',key)
    x = ("%s.%s.iops" %(HOST_REFMT,ip))
    COMMAND = '%s %s /home/nutanix/bin/query_stats.sh --type=host_perf --id=%s | egrep -w IOPS |awk -F: \'{print $2}\'' % (SSHCOMMAND, HOST, value)
    status,output=commands.getstatusoutput(COMMAND)
    EPOCH = int(time())
    val = x + ' ' +str(output)+ ' ' +str(EPOCH)
    iops_list.append(val)
iops_message = '\n'.join(iops_list) + '\n'
sock.sendall(iops_message)
print iops_message
