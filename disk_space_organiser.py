#!/usr/bin/python
#Author : Anirudh Srinivasan
__author__ = "Anirudh Srinivasan "
__copyright__ = "Copyright 2015"
__version__ = "1.0"
__maintainer__ = "Anirudh Srinivasan"
__email__ = "srianirudh@gmail.com"
__status__ = "Production"

from os import path, stat, walk, getcwd
from time import time, strftime, localtime
from humanfriendly import format_size, parse_size
from re import sub
from optparse import OptionParser
from string import maketrans, translate, letters, digits

parser = OptionParser()
parser.add_option('-d', '--days', dest='days', help='this is argument for number of days')
parser.add_option('-f', '--folder', dest='folder', help='this is the name of the directory eg. /home/nutanix')
parser.add_option('-s', '--size', dest='size', help='this is the size of the file in GB or MB or KB')
(opts, args) = parser.parse_args()

if opts.days == None or opts.folder == None or opts.size == None:
      parser.print_help()
      exit(-1)


'''Variables'''
all=maketrans('','')
nodigs=all.translate(all, letters)
digs=all.translate(all, digits)
gig = opts.size.translate(all, nodigs)
size = opts.size.translate(all, digs)


if gig == "GB":
        xsize = 1024*1024*1024
elif gig == "MB":
        xsize = 1024*1024
elif gig == "KB":
        xsize = 1024

now   = time()
sizelist = []

'''List all files older than xdays'''

print "\nList of all files older than " + str(opts.days) + " days and greater than " + str(opts.size) + " in " + str(opts.folder)
print "==========================" *len(str(opts.days)) + "==================="
for root, dirs, files in walk(opts.folder):
    for name in files:
        filename = path.join(root,name)
        try:
                if stat(filename).st_atime < now - (int(opts.days) * 86400) and stat(filename).st_size > int(size)*xsize :
                        realsize  = format_size(stat(filename).st_size)
                        print "%s" %realsize + " %s" %filename
                        sizelist.append(realsize)
        except OSError:
                pass

print "=========================" *len(str(opts.days)) + "===================="
b = []
for i in sizelist:
        b.append(parse_size(i))
print "You can save a total of %s by cleaning up the above files." %format_size(sum(b))
print "=========================" *len(str(opts.days)) + "===================="
