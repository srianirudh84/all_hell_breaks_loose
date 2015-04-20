#!/usr/bin/python
#Author: Anirudh Srinivasan
#Mar30 2014

import os
import commands
import getpass
import readline


#"""This is a python definition to add VLAN to the ESXi host """
def add_vlan():
    vlan_name = []
    vlan_no = []
    answer = str(raw_input("Is the host managed by vCenter(1) or standalone ESXi(2) host ?: "))
    if answer == "2":
       SERVER = str(raw_input("Enter the ESXi host name or IP address: "))
    elif answer == "1":
         SERVER = str(raw_input("Enter the vCenter name or IP address: "))
         VIHOST= str(raw_input("Enter the ESXi host name or IP address: "))
    #VIHOST= str(raw_input("Enter the ESXi host name or IP address: "))
    USER= str(raw_input("Enter the user name : "))
    PASSWD= getpass.getpass("Enter the password : ")
    while True:
          vlan_name.append(raw_input("Enter the vlan name: "))
          vlan_no.append(raw_input("Enter the vlan number: "))
          n = raw_input("Do you want to add more, say (y)es or (n)o: ")
          if n == "n":
             break
    vlan_dict = dict(zip(vlan_name, vlan_no))
    #vlan_list = map(int, raw_input('Enter the VLAN NO. seperated by comma: ').split(','))
    #for vlan_no in vlan_list:
    for key,value in vlan_dict.iteritems():
        if answer == "2":
           COMMAND1 = '/usr/bin/vicfg-vswitch --server=%s --username=%s --password=%s -A %s vSwitch0' %(SERVER, USER, PASSWD, key)
           COMMAND2 = '/usr/bin/vicfg-vswitch --server=%s --username=%s --password=%s -p %s -v %s vSwitch0' %(SERVER, USER, PASSWD, key, value)
           status,output = commands.getstatusoutput(COMMAND1)
           if "identifier already exists." in output :
              print "The VLAN No. already exist"
           elif "incorrect user name or password.\n" in output :
              print "May be wrong username or password, please type in correctly"
           status,output = commands.getstatusoutput(COMMAND2)
        elif answer == "1":
             #VIHOST= str(raw_input("Enter the ESXi host name or IP address: "))
             COMMAND1 = '/usr/bin/vicfg-vswitch --server=%s --username=%s --password=%s --vihost=%s -A %s vSwitch0' %(SERVER, USER, PASSWD, VIHOST, key)
             COMMAND2 = '/usr/bin/vicfg-vswitch --server=%s --username=%s --password=%s --vihost=%s -p %s -v %s vSwitch0' %(SERVER, USER, PASSWD, VIHOST, key, value)
             status,output = commands.getstatusoutput(COMMAND1)
             if "identifier already exists." in output :
                print "The VLAN No. already exist"
             elif "incorrect user name or password.\n" in output :
                print "May be wrong username or password, please type in correctly"
             status,output = commands.getstatusoutput(COMMAND2)
  
#  """This is a python definition to delete VLAN to the ESXi host """           
def del_vlan():
    vlan_name = []
    #vlan_no = []
    answer = str(raw_input("Is the host managed by vCenter(1) or standalone ESXi(2) host ?: "))
    if answer == "2":
       SERVER = str(raw_input("Enter the ESXi host name or IP address: "))
    elif answer == "1":
         SERVER = str(raw_input("Enter the vCenter  name or IP address: "))
         VIHOST= str(raw_input("Enter the ESXi host name or IP address: "))
    #SERVER = str(raw_input("Enter the server name or IP address: "))
    #VIHOST= str(raw_input("Enter the ESXi host name or IP address: "))
    USER= str(raw_input("Enter the user name : "))
    PASSWD= getpass.getpass("Enter the password : ")
    while True:
          vlan_name.append(raw_input("Enter the vlan name: "))
          #b = vlan_no.append(raw_input("Enter the vlan number: "))
          n = raw_input("Do you want to delete more, say (y)es or (n)o: ")
          if n == "n":
             break
    #vlan_dict = dict(zip(vlan_name, vlan_no))
    #vlan_list = map(int, raw_input('Enter the VLAN NO. seperated by comma: ').split(','))
    for z in vlan_name:
    #for key,value in vlan_dict.iteritems():
        if answer == "2":
           COMMAND1 = '/usr/bin/vicfg-vswitch --server=%s --username=%s --password=%s -D %s vSwitch0' %(SERVER, USER, PASSWD, z)
           status,output = commands.getstatusoutput(COMMAND1)
           if "could not be found." in output :
              print "The VLAN No. has already removed"
           elif "incorrect user name or password.\n" in output :
              print "May be wrong username or password, please type in correctly"
        elif answer == "1":
             #VIHOST= str(raw_input("Enter the ESXi host name or IP address: "))
             COMMAND1 = '/usr/bin/vicfg-vswitch --server=%s --username=%s --password=%s --vihost=%s -D %s vSwitch0' %(SERVER, USER, PASSWD, VIHOST, z)
             status,output = commands.getstatusoutput(COMMAND1)
             if "could not be found." in output :
                print "The VLAN No. has already removed"
             elif "incorrect user name or password.\n" in output :
                print "May be wrong username or password, please type in correctly"        
        
add_or_del = raw_input("Do you want to (add) or (del)ete VLAN from ESXi host? : ")
if add_or_del == "add":
   add_vlan()
elif add_or_del == "del":
   del_vlan()

