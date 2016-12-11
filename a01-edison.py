#!/usr/bin/env python
# File    : a01-edison.py ;App to control A01 via Intel Edison
# Author  : Joe McManus josephmc@alumni.cmu.edu
# Version : 0.1  12/11/2016 
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
import subprocess
try:
	import mraa
except:
	print("ERROR: Missing mraa, sure this is an Edison?")
	quit()
import pyupm_i2clcd as lcdObj


parser = argparse.ArgumentParser(description='Olympus Air A01 Control Program. (C) Joe McManus 2016')
parser.add_argument('--pid', help="Create a pid file in /var/run/a01.pid",  action="store_true")
parser.add_argument('--debug', help="Enable debug messages", action="store_true")
args=parser.parse_args()

if args.pid:
	print("Creating PID file.")
	fh=open("/var/run/a01.pid", "w")
	fh.write(str(os.getpid()))
	fh.close()

def sendLCD(msg):
    lcd.clear()
    lcd.refresh()
    lcd.setCursor(0,1)
    lcd.write(msg)
    lcd.refresh()
    time.sleep(2)
    lcd.clearScreenBuffer()
    lcd.refresh()

def getPage(air, link, headers):
	getURL=air + link
	r=requests.get(getURL, headers=headers)
	#sendLCD(r.text)

def connectA01():
    #Connect to WiFi
    netNum=subprocess.Popen("wpa_cli list_networks | awk ' /AIR/ {print $1}' ", shell=True, stdout=subprocess.PIPE).stdout.read()
    connect=subprocess.Popen("wpa_cli enable " + netNum, shell=True, stdout=subprocess.PIPE).stdout.read()
    sendLCD("AIR Net Discovered: " + str(netNum))

    sendLCD("Disconnecting other nets")
    connect=subprocess.Popen("`wpa_cli list_networks | grep  '^[0-9]' | grep -v AIR | cut -f1` ; do wpa _cli disconnect $loop  ; done" , shell=True, stdout=subprocess.PIPE).stdout.read()
    sendLCD(connect)
    sendLCD("Connecting to AIR")
    connect=subprocess.Popen("wpa_cli select_network " + netNum, shell=True, stdout=subprocess.PIPE).stdout.read()
    for i in range(10, 0, -2):
        sendLCD("Waiting " + (".")*i)
        
    sendLCD(connect)
    ip=subprocess.Popen("ifconfig wlan0 | grep inet | cut -d':' -f2 | cut -d' ' -f1", shell=True, stdout=subprocess.PIPE).stdout.read()
    sendLCD("Connected! " + ip) 
    #check mode
    sendLCD("Checking Mode")
    getPage(air, 'get_connectmode.cgi', headers)
    #set mode
    sendLCD("Setting Mode")
    getPage(air, 'switch_cameramode.cgi?mode=rec', headers)
    #Get status
    sendLCD("Getting  Mode")
    getPage(air, 'get_state.cgi', headers)
    #Set Live View
    sendLCD("Setting LiveView")
    getPage(air, 'exec_takemisc.cgi?com=startliveview&port=5555', headers)
    sendLCD("Ready to take pics.")

def disconnectA01():
    sendLCD("Reconnecting to default net")
    connect=subprocess.Popen("wpa_cli select_network 0 ", shell=True, stdout=subprocess.PIPE).stdout.read()
    for i in range(10, 0, -2):
        sendLCD("Waiting " + (".")*i)
    ip=subprocess.Popen("ifconfig wlan0 | grep inet | cut -d':' -f2 | cut -d' ' -f1", shell=True, stdout=subprocess.PIPE).stdout.read()
    sendLCD("Connected! " + ip) 
        

# setup with default values
lcd = lcdObj.EBOLED()
lcd.clear()
lcd.setTextWrap(1)
sendLCD("Air 01 App")

buttonA=mraa.Gpio(47)
buttonA.dir(mraa.DIR_IN)

buttonB=mraa.Gpio(32)
buttonB.dir(mraa.DIR_IN)

buttonUp=mraa.Gpio(46)
buttonUp.dir(mraa.DIR_IN)

buttonDown=mraa.Gpio(31)
buttonDown.dir(mraa.DIR_IN)

buttonLeft=mraa.Gpio(15)
buttonLeft.dir(mraa.DIR_IN)

buttonRight=mraa.Gpio(45)
buttonRight.dir(mraa.DIR_IN)

buttonSelect=mraa.Gpio(33)
buttonSelect.dir(mraa.DIR_IN)

buttons={ buttonA:"A", 
        buttonB: "B", 
        buttonUp: "Up",
        buttonDown: "Down",
        buttonLeft: "Left",
        buttonRight: "Right",
        buttonSelect: "Select" }



#The Olympus Air is a DHCP server that gives itself the IP below.
air='http://192.168.0.10/'

#The A01 must be given the UserAgent string of OlympusCameraKit
headers = {'user-agent': 'OlympusCameraKit', 'content-length':'4096'}


while 1:
    try:
        for button, msg in buttons.iteritems():
            if button.read() == 0 and msg == "Up": 
                connectA01()
            if button.read() == 0 and msg == "Down": 
                disconnectA01()
            if button.read() == 0 and msg == "A": 
                sendLCD("Taking Pic")
	        getPage(air, 'exec_takemotion.cgi?com=newstarttake', headers)
            if button.read() == 0 and msg == "B": 
                sendLCD("Taking 5 Pics in 15 seconds.")
		time.sleep(5)
    		for i in range(5):
                	sendLCD("Taking Pic " + str(i)+ " of 5.")
	        	getPage(air, 'exec_takemotion.cgi?com=newstarttake', headers)

        time.sleep(0.05)
            

    except KeyboardInterrupt:
        print("Exiting Sparkfun OLED Edison Block Demo")
        quit() 
            
    except Exception,e: 
        print("Error: {:s}". format(e))
        quit()
