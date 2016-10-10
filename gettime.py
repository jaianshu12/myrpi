#!/usr/bin/python
import urllib2
from urllib2 import urlopen
import time
import subprocess, os, sys

	
while(1):
	try:
		#print urllib2.urlopen("http://52.35.20.220/rpi/gettime.php").getcode()
		hiturl = urlopen("http://52.35.20.220/rpi/gettime.php",timeout=5)
		stat = hiturl.read()
		#print "stat  :" , stat
		if(stat!=None):
			f=open("/home/pi/myrpi/updatetime.txt","w+")
			f.write(str(stat))
			f.close()
			# set time
			stat = "\""+stat+"\""
			proc = subprocess.Popen(['sudo date --set '+stat], stdout=subprocess.PIPE, shell=True)
			(localfiles, err) = proc.communicate()
			break;
		#else:
			#f.write("0")
			#continue
	except:
		#print "URL Exception"
		f=open("/home/pi/myrpi/updatetime.txt","w+")
		f.write(str(0))
		f.close()
	#time.sleep(5)
