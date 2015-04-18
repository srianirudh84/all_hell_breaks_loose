#!/usr/bin/python
#Author : Anirudh Srinivasan


from os import path, stat, walk, getcwd
from time import time, strftime, localtime
from humanfriendly import format_size, parse_size
from re import sub
from optparse import OptionParser
from string import maketrans, translate, letters, digits
from boto.glacier.layer1 import Layer1
from boto.glacier.concurrent import ConcurrentUploader
from json import dumps

parser = OptionParser()
parser.add_option('-d', '--days', dest='days', help='this is argument for number of days')
parser.add_option('-f', '--folder', dest='folder', help='this is the name of the directory eg. /home/nutanix')
parser.add_option('-s', '--size', dest='size', help='this is the size of the file in GB or MB or KB')
(opts, args) = parser.parse_args()


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
target_vault_name = "Type your Vault name here"


def upload_archive:()
    '''This defenition takes care of uploading the file to the AWS Glacier one file at a time'''
    glacier_layer1 = Layer1(aws_access_key_id='Type your AWS access ID', aws_secret_access_key='Type your AWS secret access key',region_name='Pick a region to upload')
    print "\nList of all files older than " + str(opts.days) + " days and greater than " + str(opts.size) + " in " + str(opts.folder)
    print "==========================" *len(str(opts.days)) + "==================="
    for root, dirs, files in walk(opts.folder):
        for name in files:
            filename = path.join(root,name)
            try:
                if stat(filename).st_mtime < now - (int(opts.days) * 86400) and stat(filename).st_size > int(size)*xsize :
                   realsize  = format_size(stat(filename).st_size)
                   print "%s" %realsize + " %s" %filename
                   uploader = ConcurrentUploader(glacier_layer1, target_vault_name, 32*1024*1024)
                   archive_id = uploader.upload(filename, filename)
                   print("upload success! archive id: '%s'"%(archive_id))
                   return archive_id
                   sizelist.append(realsize)
            except OSError:
                pass

def vault_inventory_jobid():
    glacier_layer1 = Layer1(aws_access_key_id='Type your AWS access ID', aws_secret_access_key='Type your AWS secret access key',region_name='Pick a region to upload')
    # http://docs.aws.amazon.com/amazonglacier/latest/dev/api-initiate-job-post.html
    job_id = glacier_layer1.initiate_job(target_vault_name, {"Description":"inventory-job", "Type":"inventory-retrieval", "Format":"JSON"})
    print json.dumps(job_id, indent=2)
    return job_id
    
def vault_list_jobs():
    glacier_layer1 = Layer1(aws_access_key_id='Type your AWS access ID', aws_secret_access_key='Type your AWS secret access key',region_name='Pick a region to upload')
    out = glacier_layer1.list_jobs(target_vault_name)
    print json.dumps(out, indent=2)
    return out

def out_get_job_output():
    glacier_layer1 = Layer1(aws_access_key_id='Type your AWS access ID', aws_secret_access_key='Type your AWS secret access key',region_name='Pick a region to upload')
    hh = glacier_layer1.get_job_output(target_vault_name, job_id['JobId'])
    print json.dumps(hh, indent=2)
    return hh
    

if __name__ == '__main__':
   if opts.days == None or opts.folder == None or opts.size == None:
      parser.print_help()
      exit(-1)
   upload_archive()
   print "=========================" *len(str(opts.days)) + "===================="
   b = []
   for i in sizelist:
        b.append(parse_size(i))
   print "You have uploaded a total of %s to AWS Glacier " %format_size(sum(b))
   print "=========================" *len(str(opts.days)) + "===================="
   vault_inventory_jobid()
   vault_list_jobs()
   if out['JobList'][0]['Completed'] == True:
      out_get_job_output()
   else:
      print "The job is not currently available for download."
