#!/usr/bin/env python
# File    : a01.py ; a python app to take picture with the Olympus A01
# Author  : Joe McManus josephmc@alumni.cmu.edu
# Version : 0.1  10/01/2016 Joe McManus
# Copyright (C) 2016 Joe McManus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests
import time
import argparse

parser = argparse.ArgumentParser(description='Olympus Air A01 Control Program. (C) Joe McManus 2016')
parser.add_argument('--pid', help="Create a pid file in /var/run/a01.pid",  action="store_true")
parser.add_argument('--interval', help="Take pictures at X interval in seconds.", type=int, action="store")
parser.add_argument('--count', help="Take X pictures", type=int, action="store")
parser.add_argument('--debug', help="Enable debug messages", action="store_true")

args=parser.parse_args()

if args.pid:
	print("Creating PID file.")
	fh=open("/var/run/a01.pid", "w")
	fh.write(str(os.getpid()))
	fh.close()

if args.interval:
	print("Setting Intervalometer to take {} pictures.". format(args.interval))

if args.count:
	print("Taking a total of {} pictures." .  format(args.count))

def getPage(air, link, headers):
	getURL=air + link
	r=requests.get(getURL, headers=headers)
	if args.debug:
		print(getURL)
		print(r.text)

#The Olympus Air is a DHCP server that gives itself the IP below.
air='http://192.168.0.10/'

#The A01 must be given the UserAgent string of OlympusCameraKit
headers = {'user-agent': 'OlympusCameraKit', 'content-length':'4096'}

#Try to connect to the A01, if it fails quit
try:
	#check mode
	getPage(air, 'get_connectmode.cgi', headers)
except:
	print("ERROR: Unable to reach air at : " + air)
	quit()

#set mode
getPage(air, 'switch_cameramode.cgi?mode=rec', headers)

#Get status
getPage(air, 'get_state.cgi', headers)

#Set Live View
getPage(air, 'exec_takemisc.cgi?com=startliveview&port=5555', headers)

#Take one picture and exit
if not args.count:
	#Take a picture
	print("Taking 1 photo.")
	getPage(air, 'exec_takemotion.cgi?com=newstarttake', headers)
	quit()

#Take pics at specified interval
if args.count: 
	i=1
	while i <= args.count:
		print("Taking picture {} of {} ". format(i, args.count))
		getPage(air, 'exec_takemotion.cgi?com=newstarttake', headers)
		if args.interval and args.count != i:
			print("Sleeping for {} seconds.". format(args.interval))
			time.sleep(args.interval)
		i=i+1

