#!/usr/bin/env python
#Author: Anirudh Srinivasan
#Date : Feb 26 2016


# Import modules
import os
import time
import shutil

# Define variables
xdays=2
src_path="/export/sdb1/backup/ts_backup/"
dest_path="/backup/dev-thoughtspot/"
now=time.time()


#First remove old file from dest_path
os.chdir(dest_path)
dir1 = [ name for name in os.listdir(dest_path) if os.path.isdir(os.path.join(dest_path, name)) ]
for name in dir1:
                '''If the directory is less than xdays old then do not delete it'''
                if not os.stat(name).st_mtime > now - (xdays * 86400):
                        print "Removing the following directory %s" %os.path.join(dest_path, name)
                        shutil.rmtree(name)

# List all files newer than xdays
os.chdir(src_path)
dir2 = [ name for name in os.listdir(src_path) if os.path.isdir(os.path.join(src_path, name)) ]
for name in dir2:
                '''If the directory is less than xdays old and if it exist in dest_path then do not copy it'''
                if os.stat(name).st_mtime > now - (xdays * 86400):
                        if not os.path.exists(os.path.join(dest_path, name)):
                                print "Moving the %s to %s" %(os.path.join(src_path, name),  os.path.join(dest_path, name))
                                shutil.copytree(os.path.join(src_path, name), os.path.join(dest_path, name))
                        else:
                                pass
