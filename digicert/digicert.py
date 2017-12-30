#!/usr/bin/python


import json
import requests
import glob
import sys
from os.path import expanduser
from os import chdir
from os import mkdir
from os import environ
from shlex import split
from subprocess import call
from pprint import pprint

account_id = environ.get("account_id")
api_key = environ.get("api_key")

def get_info(order):
	URL = 'https://api.digicert.com/order/%s' %(order)
	r = session.get(URL)
	return r.json()
	
def post_info(data):
	URL = 'https://api.digicert.com/enterprise/certificate/ssl'
	head = {'User-Agent': 'MyAPIConsumer/0.42', 'Content-Length': '496', 'Content-Type': 'application/vnd.digicert.rest-v1+json', 'Authorization': 'Basic MDAxMDA3OnNreWZhbGw='}
	r = session.post(URL, headers=head, data=json.dumps(data))
	return r.json()
	
def approve_order(request_id):
	URL = 'https://api.digicert.com/request/%s' %(request_id)
	head = {'User-Agent': 'MyAPIConsumer/0.42', 'X-HTTP-Method-Override': 'APPROVE', 'Accept': 'application/vnd.digicert.rest-v1+json', 'Authorization': 'Basic MDAxMDA3OnNreWZhbGw='}
	r = session.post(URL, headers=head)
	return r.json()
	
def create_csr(common_name):
	gen_csr = input("Do you have your own CSR? type y or n:  ")
	if gen_csr == 'y':
		csr_file_path = input("Please provide absolute path to the csr file: ")
		csr_file = csr_file_path+"/*.csr"
		for filename in glob.glob(csr_file):
			with open(filename, 'r') as f:
				csr = f.read().strip('\n')
				return csr
	if gen_csr == 'n':
		home = expanduser("~/")
		path = home+common_name
		mkdir(path)
		chdir(path)
		openssl_cmd = call(split('openssl req -new -newkey rsa:2048 -nodes -out %s.csr -keyout %s.key -subj "/C=US/ST=California/L=San Jose/O=xyz.INC/CN=%s"' %(common_name,common_name,common_name)))
		csr_file = path+"/*.csr"
		for filename in glob.glob(csr_file):
			with open(filename, 'r') as f:
				csr = f.read().strip('\n')
				return csr

def main():
	action = input("Do you want to 'GET' or 'POST': ")
	if action == 'POST':
		common_name = input("Enter the FQDN of the hostnames: ")
		no_of_sans = int(input("How many SANs hostnames: "))
		sans = []
		count = 0
		while count < no_of_sans:
			sans.append(input("Enter Hostname: "))
			count += 1
		comments = input("Enter the comment of the hostnames: ")
		server_type = input("Is it Apache(2) or Nginx(45), please select the number:  ")
		validity = input("Is it 1,2 or 3 years, remember there is a price variation for each year: ")
		data = {"org_name":"XYZ, Inc.","org_addr1":"xyz, 4th st","org_city":"San Jose","org_state":"California","org_zip":"95110","org_country":"us"}
		a = create_csr(common_name)
		data.update({'common_name': common_name, 'sans': sans, 'comments': comments, 'server_type': server_type, 'validity': validity, 'csr': a})
		print (json.dumps(data, indent=1))
		ans = input("Is the above json file format correct , type y or n : ")
		if ans == 'y':
			post = post_info(data)
			print (post['request_id'])
			#approve = input("Do you want to approve the cert, type y or n : ")
			#if approve == 'y':
				#apprv = approve_order(request_id)
				#print (apprv)
			#if approve == 'n':
				#sys.exit(-1)
		if ans == 'n':
			sys.exit(-1)

	if action == 'GET':
		order = input("Enter the order number: ")
		get = get_info(order)
		pprint (get)

if __name__ == '__main__':
	session = requests.Session()
	session.auth = (account_id, api_key)
	main()
	session.close()
