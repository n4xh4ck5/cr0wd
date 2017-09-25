#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import sys
import xlsxwriter
from time import sleep
import urllib2
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#Disable warning by SSL certificate
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

search = ['email','domain','ip','antivirus','file']

### EXPORT RESULTS ###
def ExportResults(data,output):
	# Start from the first cell. Rows and columns are zero indexed.
	row = 0
	col = 0
	try:
		if output == 'js': 
			#Export the results in json format
			print "Exporting the results in an json"
			with open ('output.json','w') as f:
				json.dump(data,f)
		elif (output == 'xl'):
			#Export the results in excel format
			print "\nExporting the results in an excel"
			# Create a workbook and add a worksheet.
			workbook = xlsxwriter.Workbook('output.xlsx')
			worksheet = workbook.add_worksheet()
			worksheet.write(row, col, "Domain")
			row +=1
			for domain in data:
				col = 0
				worksheet.write(row, col, domain)
				row += 1
			#close the excel
			workbook.close()
		else:
			exit(1)
	except Exception as e:
		print e 

### SEARCH EMAIL ###
def SearchEmail(target):
	url="https://www.threatcrowd.org/searchApi/v2/"+search[0]+"/report/?email="+target
	array_domains_email = []
	export = True
	resp = None
	try:
		response = requests.get (url,allow_redirects=False, timeout=7,verify=False)
		data = json.loads(response.text)
		if (data['domains']) < 1:
			print "\n Don't find any information about this email"
		else:
			for domain in data['domains']:
				print "\n\t- " + domain
				array_domains_email.append(domain)
			print "\nDo you like to export results(Y/N)"
			resp = raw_input().lower()
			if resp == 'y':
				while export:
					print "\nChoose the type of export:json(js) or xlsx(xl):"
					export = raw_input().lower()
					if export == 'js' or export == 'xl':
						ExportResults(array_domains_email,export)
						export = None
					else:
						print "Incorrect type of export.Try again it"
		sleep (2)
	except Exception as e:
		print e
### SEARCH DOMAIN ###
def SearchDomain (target):
	data = None
	resp = None
	export = True
	array_subdomains = []
	url = "https://www.threatcrowd.org/searchApi/v2/"+search[1]+"/report/?domain="+target
	try:
		response = requests.get (url,allow_redirects=False, timeout=7,verify=False)
		data = json.loads(response.text)
		for subdomain in data['subdomains']:
			print "\n\t- " + subdomain
			array_subdomains.append(subdomain)
		print "\nDo you like to export results(Y/N)"
		resp = raw_input().lower()
		if resp == 'y':
			while export:
				print "\nChoose the type of export:json(js) or xlsx(xl):"
				export = raw_input().lower()
				if export == 'js' or export == 'xl':
					ExportResults(array_subdomains,export)
					export = None
				else:
					print "Incorrect type of export.Try again it"
		#Do a sleep during 2 seconds to respect the limit of the API
		sleep (2)
	except Exception as e:
		print e

### SEARCH IP ###
def SearchIP (target):
	data = None
	url = "https://www.threatcrowd.org/searchApi/v2/"+search[2]+"/report/?ip="+target
	array_domains = []
	export = True
	try:
		response = requests.get (url,allow_redirects=False, timeout=7,verify=False)
		data = json.loads(response.text)
		for domain in data['resolutions']:

			print "\n\t- " + domain['domain']
			array_domains.append(domain['domain'])

		print "\nDo you like to export results(Y/N)"
		resp = raw_input().lower()
		if resp == 'y':
			while export:
				print "\nChoose the type of export:json(js) or xlsx(xl):"
				export = raw_input().lower()
				if export == 'js' or export == 'xl':
					ExportResults(array_domains,export)
					export = None
				else:
					print "Incorrect type of export. Try again it"
		#Do a sleep during 2 seconds to respect the limit of the API
		sleep (2)
	except Exception as e:
		print e


def menu ():
	resp=True
	while resp:
	    print """
	    1. Search email
	    2. Search info about IP address
	    3. Search info about domain
	    4. Exit/Quit
	    """
	    print "What would you like to do?"
	    resp=raw_input ()
	    if resp =="1":
	      print "\nSearch email"
	      target = raw_input()
	      SearchEmail(target)
	    elif resp=="2":
	      print "\n Search info about IP address"
	      print "\n Enter the IP: "
	      target = raw_input()
	      SearchIP (target)
	    elif resp=="3":
	      print "\n Search info about domain"
	      print "\n Enter the domain: "
	      target = raw_input()
	      SearchDomain (target)
	    elif resp=="4":
	      print "\n Goodbye"
	      resp = None
	    else:
	       print"\n Not Valid Choice Try again"

""" FUNCTION BANNER """
def banner ():
	print """
		       _..._                                                      
	    .-'_..._''.                                     _______       
	  .' .'      '.\                                    \  ___ `'.    
	 / .'                                         _     _' |--.\  \   
	. '             .-,.--.     .-''` ''-.  /\    \\   //| |    \  '  
	| |             |  .-. |  .'          '.`\\  //\\ // | |     |  ' 
	| |             | |  | | /              ` \`//  \'/  | |     |  | 
	. '             | |  | |'                ' \|   |/   | |     ' .' 
	 \ '.          .| |  '- |         .-.    |  '        | |___.' /'  
	  '. `._____.-'/| |     .        |   |   .          /_______.'/   
	    `-.______ / | |      .       '._.'  /           \_______|/    
	             `  |_|       '._         .'                          
	                             '-....-'`                        """
	print "\n"
	print """** Tool to interact the API ThreatCrowd
	** Version 1.0
	** Author: Ignacio Brihuega Rodriguez a.k.a N4xh4ck5
	** Github: https://github.com/n4xh4ck5/
	** DISCLAMER This tool was developed for educational goals. 
	** The author is not responsible for using to others goals.
	** A high power, carries a high responsibility!"""

def help ():
	print  """ \nThis script interacts the API ThreatCrowd

			Example of usage: python cr0wd.py """

""" FUNCTION MAIN """
def main (argv):

	banner()
	#call help
	help()
	#Call Menu
	menu ()

# CALL MAIN
if __name__ == "__main__":
	main(sys.argv[1:])