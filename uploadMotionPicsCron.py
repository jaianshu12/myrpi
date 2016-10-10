#!/usr/bin/python

import os, time, sys, cv2
import urllib2
from urllib2 import urlopen
import numpy as np
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import requests
import subprocess


font = cv2.FONT_HERSHEY_DUPLEX
main_url = "http://52.35.20.220/rpi/"
register_openers()
def uploadAndRemove(imageName):
# Subroutine to upload pic using HTTP protocol
	#register_openers()
	with open(imageName, 'r') as f:
		time.sleep(1)
		datagen, headers = multipart_encode({"file": f})
		request = urllib2.Request(main_url+"arrangePic.php",datagen, headers)
		response = urllib2.urlopen(request)		
		myname = "/home/pi/myrpi/local_motion_storage/"+str(response.read())
		print "====="+myname+"=========="
		os.remove(myname)
 

try: 
	while(1): # this runs the script infinitely.
		proc = subprocess.Popen(['ls -at /home/pi/myrpi/local_motion_storage| grep -v "^\."'], stdout=subprocess.PIPE, shell=True)
		(localfiles, err) = proc.communicate()
		local_fileName = localfiles.split("\n")[:-1]
		print local_fileName
		for img in local_fileName:
			uploadAndRemove("/home/pi/myrpi/local_motion_storage/" + img)
			
except KeyboardInterrupt:
	print "KeyBoardInterrupt"
	
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise 

finally:
	print "Done from Cron"
