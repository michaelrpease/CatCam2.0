'''
This is a program written in Python to detect the motion of my cats in order
to record their behavior throughout the day.
'''

import RPi.GPIO as GPIO
import time
import picamera
import datetime
import signal
import subprocess

GPIO.setmode(GPIO.BCM)
pirPin = 7
GPIO.setup(pirPin, GPIO.IN)
cam = picamera.PiCamera()

def getFileName():
	return datetime.datetime.now().strftime("%y-%m-%d_%H.%M.%S")

def motion(pirPin):
	print "Motion Detected"
	fileName = getFileName()
	print "Recording..."
	cam.start_recording(fileName + ".h264")
	cam.wait_recording(60)
	cam.stop_recording()
	print "Recording complete"

	print "Converting file..."
	subprocess.call(["MP4Box", "-fps", "30", "-add", fileName + ".h264",fileName + ".mp4"])
	subprocess.call(["mv", fileName + ".mp4", "Recordings"]) 
	print "Conversion complete"
	print "Scanning..."

print "CatCam is starting..."
time.sleep(2)
print "Ready - (CTRL+C to exit)"

try:
	print "Scanning..."
	GPIO.add_event_detect(pirPin, GPIO.RISING, callback = motion)
	while 1:
		time.sleep(60)
except KeyboardInterrupt:
	print "\nCatCam is shutting down..."
	time.sleep(2)
	GPIO.cleanup()
	cam.close()
	print "Goodbye"
