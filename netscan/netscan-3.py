#!/usr/bin/python


from libnmap.parser import NmapParser
from libnmap.process import NmapProcess
from sys import argv
import time
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-n', '--network',action="append",dest="my_network", help='Please type atleast one subnet of the type x.x.x.x/x')
parser.add_option('-t', '--time', dest="custom_time", help='custom time in sec')
(options, args) = parser.parse_args()

def ip_info(subnet):
    nm = NmapProcess(subnet, options="-Pn  -O")
    rc = nm.sudo_run()
    if nm.rc == 0:
        rep = NmapParser.parse(nm.stdout)
        for host in rep.hosts:
            if host.is_up():
                print("IP Address: {0}".format(host.address))
                if host.os_fingerprinted:
                    for osm in host.os.osmatches:
                        print("OS Type: {0}".format(osm.name))
                        print ("Last seen timestamp: {0}\n"  .format(host.lastboot))
    else:
        print (nm.stderr)

def main():
    try:
        while True:
            for network in options.my_network:
                ip_info(network)
                time.sleep(float(options.custom_time))
    except KeyboardInterrupt:
        print("Good Bye!")

if __name__ == '__main__':
    if options.my_network == None or options.custom_time == None:
        parser.print_help()
        exit(-1)
    else:
        main()
        #print options.my_network
        #print options.custom_time
