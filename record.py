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

#GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
pirPin = 4
ledPin = 12
GPIO.setup(pirPin, GPIO.IN)
GPIO.setup(ledPin, GPIO.OUT)
cam = picamera.PiCamera()

def getFileName():
	return datetime.datetime.now().strftime("%y-%m-%d_%H.%M.%S")

def motion(pirPin):
	GPIO.output(ledPin, GPIO.HIGH)
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
	subprocess.call(["rm", fileName + ".h264"])
	GPIO.output(ledPin, GPIO.LOW)
	print "Ready - (Press button to exit)"
	print "Scanning..."

print "CatCam is starting..."
time.sleep(2)

try:
	print "Ready - (Press button to exit)"
	print "Scanning..."
	GPIO.add_event_detect(pirPin, GPIO.RISING, callback = motion, bouncetime = 63000)
	while True:
		pass

except OSError as e:
	GPIO.cleanup()
	cam.close()
	print "CatCam closed properly"
