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

#The Olympus Air is a DHCP server that gives itself the IP below.
air='http://192.168.0.10/'

#The A01 must be given the UserAgent string of OlympusCameraKit
headers = {'user-agent': 'OlympusCameraKit', 'content-length':'4096'}

#Try to connect to the A01, if it fails quit
try:
	#check mode
	getURL=air + 'get_connectmode.cgi'
	print(getURL)
	r=requests.get(getURL, headers=headers)
	print(r.text)
except:
	print("ERROR: Unable to reach air at : " + air)
	quit()

#set mode
getURL=air + 'switch_cameramode.cgi?mode=rec'
print(getURL)
r = requests.get(getURL, headers=headers)
print(r.text)

#Get status
getURL=air + 'get_state.cgi'
print(getURL)
r = requests.get(getURL, headers=headers)
print(r.text)

#Set Live View
getURL=air + 'exec_takemisc.cgi?com=startliveview&port=5555'
print(getURL)
r = requests.get(getURL, headers=headers)
print(r.text)

#Try to take a picture
#xml="""<?xml version='1.0' encoding='utf-8'?>
#<>"""
try:
	getURL=air + 'exec_takemotion.cgi?com=newstarttake'
	print(getURL)
	r=requests.get(getURL, headers=headers)
	print(r.text)
except: 
	print("ERROR: Unable to take photo")
	quit()
