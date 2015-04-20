#!/usr/bin/python

from fabric.api import *
import readline


""" Host defenition """
#def anirudh_dev():
#        env.user = "root"
#        env.hosts = ['type hostname here']

#def anirudh():
#        env.user = "anirudh"
#        env.password = "type password here"
#        env.hosts = ['type hostname here']
#env.hosts = ['type hostname here']
env.user = "it"
env.password = "type password here"


""" Command defenition """
def useradd():
	usr = raw_input("Enter the username: ")
	full_name = raw_input("Enter the user's full name: ")
	run('/usr/bin/sudo /usr/sbin/useradd -m -d /home/%s -c "%s" -s /bin/bash %s' %(usr,full_name,usr))
	run('/bin/echo %s:<type password here> | /usr/bin/sudo /usr/sbin/chpasswd' %usr)
	run('/usr/bin/sudo /usr/bin/chage -d 0 %s' %usr)

""" Command defenition """
def snmp_stop():
        run('/bin/bash -l -c "/usr/bin/sudo /sbin/service snmpd stop"')	

def run_script():
	run('/bin/bash -l -c "script here"')

def snmp_start():
        run('/bin/bash -l -c "/usr/bin/sudo /sbin/service snmpd start"')
