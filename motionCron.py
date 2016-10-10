#!/usr/bin/python
import numpy as np
import cv2
import sys
import urllib2
from urllib2 import urlopen
from random import choice
from string import ascii_lowercase
import time
import thread

#number of images
#num = int(sys.argv[1])

#Output file name
#outfile = sys.argv[1]

#Initialize camera from camera port 0
cap = cv2.VideoCapture(0)

#counter
ctr = 0
flag = 0
main_url = "http://52.35.20.220/rpi/"
status_url = main_url+"flags/motion.txt" 
font = cv2.FONT_HERSHEY_DUPLEX

while(1):	
	try: 
		hiturl = urlopen(status_url,timeout=5)
		stat = hiturl.read()
		print("motion status: ", stat)
		if(stat =="1" or stat =="1\n"):
			flag = 0
			#print cap.isOpened()
			if(cap.isOpened()==False):
				cap = cv2.VideoCapture(0)
			if(cap.isOpened()):
				#print "ffffff"
				if(flag == 0):
						# Capture first frame
						ret, frame1 = cap.read()
						gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
					
				ret, frame2 = cap.read()
				gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

				#diff of two images
				diff = cv2.absdiff(gray1,gray2)
			 
				#Applying thresholding
				thresh = cv2.threshold(diff,10,255,cv2.THRESH_BINARY_INV)
				#print thresh[1]
				h, w = frame2.shape[:2]
				nb=0
				for i in range(0,h,4):
					for j in range(0,w,4):
						if(thresh[1][i][j] == 0.0):
							nb += 1
				avg = nb*16*100.0/(w*h)
				print avg
				if(avg > 8):
					print "Something is moving"
					seq = ("R", time.strftime("%Y%m%d%H%M%S"), ''.join(choice(ascii_lowercase) for i in range(5)))
					outfile = ''.join( seq ) # output filename i.e. pic name
					print "111111",outfile
					height,width,channels = frame2.shape
					localtime = time.asctime( time.localtime(time.time()) )
					#print "222222",localtime
					cv2.putText(frame2,str(localtime),(width/4,height-15),font,1,(0,0,255),2,cv2.LINE_AA)
					print outfile
					cv2.imwrite("local_motion_storage/"+outfile+".jpg",frame2)
					ctr += 1
				flag = 1 
				gray1 = gray2
			
			# Display the resulting frame
			#cv2.imshow('frame',frame2)
			if cv2.waitKey(10) & 0xFF == ord('q'):
				break
				
		else:
			# When everything done, release the capture
			if(cap.isOpened()):
				cap.release()
			#cv2.destroyAllWindows()
			
	except KeyboardInterrupt:
		if(cap.isOpened()):
			cap.release()
		print "KeyBoardInterrupt"
		break
	except:
		continue
	#finally:
		#print "Done from Motion Cron"

