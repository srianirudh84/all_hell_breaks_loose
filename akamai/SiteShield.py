#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 15:30:46 2016

@author: anirudh
"""

import ipaddress
#Test Values
#akamai_ip_list = ['10.4.10.0/24', '10.4.8.0/24', '10.4.6.0/24']
#my_ip = ['10.4.8.16', '10.3.3.1', '10.4.10.10']
akamai_ip_list = ['104.104.245.0/24', '104.112.235.0/24', '104.71.131.0/24', '104.96.220.0/24', '104.97.78.0/24', '184.25.157.0/24', '184.26.44.0/24', '184.28.127.0/24', '184.28.17.0/24', '184.51.199.0/24', '184.84.239.0/24', '2.16.106.0/24', '2.18.240.0/24', '23.14.94.0/24','23.205.170.0/24','23.215.131.0/24', '23.216.10.0/24','23.45.235.0/24','23.62.239.0/24', '23.67.253.0/24', '23.79.240.0/24', '72.246.150.0/24', '72.246.216.0/24', '72.246.52.0/24', '96.17.70.0/24']
my_ip = []
for line in open('/Users/anirudh/r2d2/r2d2_nginx.access_ssl.log.6'):
    line = line.split(' ')
    if "akamai.net(ghost)" in line:
        ip=line[0]
        my_ip.append(ip)

#print (akamai_ip_list)
list_from_log =  list((set(my_ip)))
   
whitelist = []
for i in list_from_log:
   true_or_false_list = []
   for j in akamai_ip_list:
       out = ipaddress.ip_address(i) in ipaddress.ip_network(j)
       true_or_false_list.append(out)
   if True in true_or_false_list:
       pass
   else:
       whitelist.append(i)
       
print  (whitelist)
