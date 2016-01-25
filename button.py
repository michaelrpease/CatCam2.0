import RPi.GPIO as GPIO
import time
import subprocess
import signal
import os


#GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
ledPin = 18
buttonPin = 23
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN)

btnOn = 0

print "Press button to start CatCam"

def light(buttonPin):

	global btnOn
	btnOn = not btnOn

	if btnOn:
		GPIO.output(ledPin, GPIO.HIGH)
		args = ["python", "record.py"]
		global p
		p = subprocess.Popen(args)

	else:
		GPIO.output(ledPin, GPIO.LOW)
		p.kill()
		print "CatCam is shutting down..."
		print "Goodbye"
		

try:

	GPIO.add_event_detect(buttonPin, GPIO.RISING, callback = light, bouncetime=300)
	while True:
		pass

except KeyboardInterrupt():
	pass

except:
	pass

finally:
	print ""
	GPIO.cleanup()
