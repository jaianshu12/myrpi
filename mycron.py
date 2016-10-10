#!/usr/bin/python

# Polling script...keeps on contacting server and as soon as get signal from server [Take Pic button pressed from App], takes the pic
# For taking the Pic - takePicture.py <no. of Pic> <name of Pic>

import os, time, sys, re, cv2
import fileinput
from random import choice
from string import ascii_lowercase
import urllib2
from urllib2 import urlopen
import numpy as np
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import requests
import subprocess

font = cv2.FONT_HERSHEY_DUPLEX
# main_url = "http://srinivastech.in/anshul/"
main_url = "http://52.35.20.220/rpi/"
status_url = main_url+"flags/status.txt" 
pics_url = main_url+"uploaded_pics/" 
num = 5 # No of photos to take
ctr = 0 # Initialize the counter to Zero.	

def uploadpicfromHTTP(imageName):
# Subroutine to upload pic using HTTP protocol
	register_openers()
	with open(imageName, 'r') as f:
		datagen, headers = multipart_encode({"file": f})
		request = urllib2.Request(main_url+"getpic.php",datagen, headers)
		response = urllib2.urlopen(request)

cap = cv2.VideoCapture(0) #Initialize camera from camera port 0
while(1):	
	try: 
		# ======================== PART 1: Check Status ==================================== 
		while(1): # this runs the script infinitely.
			hiturl = urlopen(status_url,timeout=10)
			stat = hiturl.read()
			print("flag stat: ", stat)
			if(stat =="R" or stat =="R\n"):
				proc = subprocess.Popen(['python testservo.py R'], stdout=subprocess.PIPE, shell=True)
				(localfiles, err) = proc.communicate()
				stat="1"
			if(stat =="L" or stat =="L\n"):
				proc = subprocess.Popen(['python testservo.py L'], stdout=subprocess.PIPE, shell=True)
				(localfiles, err) = proc.communicate()
				stat="1"
			if(stat =="C" or stat =="C\n"):
				proc = subprocess.Popen(['python testservo.py C'], stdout=subprocess.PIPE, shell=True)
				(localfiles, err) = proc.communicate()
				stat="1"
				
			if (stat == "1" or stat == "1\n"):
				print "inside flag"
				seq = ("R", time.strftime("%Y%m%d%H%M%S"), ''.join(choice(ascii_lowercase) for i in range(5)))
				outfile = ''.join( seq ) # output filename i.e. pic name
				# ======================== PART 2: Take Pics ====================================  
				
				while(cap.isOpened()):
					# Capture frame-by-frame
					ret, frame = cap.read()
					if(ctr < num):
						if(ctr == num-1):
							print "inside cv2"
							#urllib2.urlopen(main_url+'updateStatus.php')
							height,width,channels = frame.shape
							localtime = time.asctime( time.localtime(time.time()) )
							cv2.putText(frame,str(localtime),(width/4,height-15),font,1,(0,0,255),2,cv2.LINE_AA)
							cv2.imwrite("local_storage/"+outfile+".jpg",frame)
					else:
						break	
					ctr += 1
				
				ctr=0
				print "o/p file : " + outfile
				# ======================== PART 3: Upload pics to server ==================================== 
				proc = subprocess.Popen(['ls -at /home/pi/myrpi/local_storage| grep -v "^\."'], stdout=subprocess.PIPE, shell=True)
				(localfiles, err) = proc.communicate()
				#print "program output:", localfiles
				# exit()
				local_fileName = localfiles.split("\n")[:-1]
				hiturl = urlopen(pics_url)
				stat = hiturl.read()
				cnt = stat.count('.jpg<')
				server_fileName = re.findall("href=\"(\w+.jpg)\"", stat)
				if(set(local_fileName).issuperset(set(server_fileName))):	
					uploadset = (set(local_fileName) - set(server_fileName))
				else:
					uploadset = (set(server_fileName) - set(local_fileName))
				
				uploadList = list(uploadset)
				# print "Server Files: " , server_fileName
				# print "Local Files: ", local_fileName
				print "Files to be uploaded : " ,uploadList
				for img in uploadList:
					uploadpicfromHTTP("/home/pi/myrpi/local_storage/" + img)
					print "uploaded ", img
				#call GCM service
				urllib2.urlopen(main_url+'sendGCMMessage.php')
				#Update the status back to '0'.
				urllib2.urlopen(main_url+'updateStatus.php') 
				#cap.release()
			else:
				continue
	except KeyboardInterrupt:
		if(cap.isOpened()):
			cap.release()
		print "KeyBoardInterrupt"
		break
	except:
		continue
	finally:
		print "Done from Cron"
