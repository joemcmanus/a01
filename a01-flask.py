#!/usr/bin/env python
# File    : a01.py ; a python app to take picture with the Olympus A01
# Author  : Joe McManus josephmc@alumni.cmu.edu
# Version : 0.3  10/21/2016 Joe McManus
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
import re
import os
from flask import Flask, render_template, Markup, request, make_response, send_file

def getPage(air, link, headers):
	getURL=air + link
	r=requests.get(getURL, headers=headers)
	return(r.text)

def getThumb(air, imageName, headers):
	getPage(air, 'switch_cameramode.cgi?mode=standalone', headers)
	getPage(air, 'switch_cameramode.cgi?mode=play', headers)
	getURL=air + "get_thumbnail.cgi?DIR=/DCIM/100OLYMP/" + imageName
	r=requests.get(getURL, headers=headers, stream=True)
	with open('static/thumbs/' + imageName, 'wb') as fh:
		for chunk in r.iter_content(1024):
			fh.write(chunk)
	fh.close()
	getPage(air, 'switch_cameramode.cgi?mode=standalone', headers)
	getPage(air, 'switch_cameramode.cgi?mode=rec', headers)
	getPage(air, 'exec_takemisc.cgi?com=startliveview&port=5555', headers)

def setupConnection():
	#Try to connect to the A01, if it fails quit
	try:
		#check mode
		print("Trying to connect to A01")
		getPage(air, 'get_connectmode.cgi', headers)
	except:
		print("ERROR: Unable to reach air at : " + air)
		print("ERROR: Make sure you are connected to the Air Wifi. ")
		print("ERROR: The SSID is something like AIR-A01-MAC")
		quit()

	#set mode
	print("Setting A01 up for WiFi Control")
	getPage(air, 'switch_cameramode.cgi?mode=standalone', headers)
	getPage(air, 'switch_cameramode.cgi?mode=rec', headers)

	#Set Live View
	getPage(air, 'exec_takemisc.cgi?com=startliveview&port=5555', headers)

	#Next we will create thumbnail and download directories
	if not os.path.exists('static/thumbs'):
		os.mkdir('static/thumbs')

	if not os.path.exists('static/images'):
		os.mkdir('static/images')

app = Flask(__name__)

#The Olympus Air is a DHCP server that gives itself the IP below.
air='http://192.168.0.10/'

#The A01 must be given the UserAgent string of OlympusCameraKit
headers = {'user-agent': 'OlympusCameraKit', 'content-length':'4096'}

setupConnection()

@app.route('/')
def index():
	bodyText=Markup('''<a href=/takePic> Take a picture</a><br>
	<a href=/getImageList> Download Images </a><br>		
	<a href=/setInt> Setup Intervalometer </a><br>		
	<a href=/getStatus> Check Status </a><br>		
	<a href=/clearImages> Remove Images From SD Card </a><br>		
	''')
	return render_template('templatecss.html', bodyText=bodyText)

@app.route('/getStatus')
def getStatus():
	bodyText=getPage(air, 'get_state.cgi', headers)
	return render_template('templatecss.html', bodyText=bodyText)

@app.route('/takePic')
def takePic():
	imageInfo=getPage(air, 'exec_takemotion.cgi?com=newstarttake', headers)
	bodyText="Taking a photo " + imageInfo 
	return render_template('templatecss.html', bodyText=bodyText)
	
@app.route('/getImageList')
def getImageList():
	bodyText=("Images on A01 <br>")
	response= getPage(air , 'get_imglist.cgi?DIR=/DCIM/100OLYMP', headers)
	results=re.findall("P.\d*.JPG", response)
	for result in results:
		getThumb(air, result, headers)
		bodyText=bodyText + "<img src=/static/thumbs/" + result + "> <a href=getImage/" + result + "> " +  result + " </a> <br>\n"
	bodyText=Markup(bodyText)
	return render_template('templatecss.html', bodyText=bodyText)

@app.route('/getImage/<imageName>')
def getImage(imageName):
	getURL=air + "/DCIM/100OLYMP/" + imageName
	r=requests.get(getURL, headers=headers, stream=True)
	with open('static/images/' + imageName, 'wb') as fh: 
		for chunk in r.iter_content(1024):
			fh.write(chunk)
	fh.close()
	bodyText=Markup("Downloaded image <a href=" + imageName + ">" + imageName + "</a> <br> <img src=/static/images/" + imageName + " width=800 height=600> <br>")
	return render_template('templatecss.html', bodyText=bodyText)

@app.route('/clearImages')
def clearImages():
	getPage(air, 'switch_cameramode.cgi?mode=standalone', headers)
	getPage(air, 'switch_cameramode.cgi?mode=play', headers)
	getPage(air, 'switch_cameramode.cgi?mode=playmaintenance', headers)
	bodyText=("Clearing Images on A01 <br> \n")
	response= getPage(air , 'get_imglist.cgi?DIR=/DCIM/100OLYMP', headers)
	results=re.findall("P.\d*.JPG", response)
	for result in results:
		link='exec_erase.cgi?DIR=/DCIM/100OLYMP/' + result
		print(getPage(air, link, headers))
		bodyText=bodyText + "Erasing : " + link + " <br> \n"

		#Delete local files
		if os.path.isfile('static/thumbs/'+ result):
			os.remove('static/thumbs/'+ result)
		if os.path.isfile('static/images/'+ result):
			os.remove('static/images/'+ result)

	bodyText=Markup(bodyText)
	getPage(air, 'switch_cameramode.cgi?mode=standalone', headers)
	getPage(air, 'switch_cameramode.cgi?mode=rec', headers)
	getPage(air, 'exec_takemisc.cgi?com=startliveview&port=5555', headers)
	return render_template('templatecss.html', bodyText=bodyText)

@app.route('/about')
def about():
	bodyText=Markup(''' This is a simple web framework to display functionality of the <br>
	Olympus Air A01 Open Platform Camera <br>. 
	<br>
	Written by Joe McManus josephmc@alumni.cmu.edu and released under the GPL. Copywrite Joe McManus 2016 <br>
	''')
	return render_template('templatecss.html', bodyText=bodyText)

@app.route('/setInt')
def setInt():
	bodyText="Not ready yet, check back soon. <br> In the meantime use the command line version."
	return render_template('templatecss.html', bodyText=bodyText)

@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(500)
def errorpage(e):
	bodyText="Oops, something went wrong"
	return render_template('templatecss.html', bodyText=bodyText) 

@app.after_request
def add_no_cache(response):
	response.cache_control.no_cache = True
	response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
	response.headers['Cache-Control'] = 'public, max-age=0'
	return response

if __name__ == '__main__':
	app.debug = False
	app.run(host='0.0.0.0', port=80)

