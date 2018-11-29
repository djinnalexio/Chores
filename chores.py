#!/usr/bin/python
# -*- coding: utf-8 -*-

"By Andre Akue"

import RPi.GPIO as GPIO
import time
from os import system
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)

class lights:

    def __init__(self,color_name,color_pin):
		self.name = color_name
		self.pin = color_pin
		GPIO.setup(self.pin, GPIO.OUT, initial = 1)

	def check_state(self):
		if GPIO.input(self.pin):
			print ("\tThe " + self.name + " light is on.")
		elif GPIO.input(self.pin) == 0:
			print ("\tThe " + self.name + " light is off.")

	def toggle_switch(self,color):
		if color == self.name:
			if GPIO.input(self.pin):
				GPIO.output(self.pin,0)
				print ("\tThe " + self.name + " light was turned off.")
			elif GPIO.input(self.pin) == 0:
				GPIO.output(self.pin,1)
				print ("\tThe " + self.name + " light was turned on.")
		else:
			pass

	def blinking(self,color):
		if color == self.name:
			system('clear')
			stp = time.time() ; etp = time.time() + duration # stp/etp = starting / ending time pattern
			while time.time() < etp:
				print ("\n\n\n\n\n\n\n\tThe " + self.name + " light is blinking.")
				print "\n\n\t\t%i/%i seconds" % (int(time.time() - stp),duration)
				GPIO.output(self.pin,0)
				time.sleep(0.5/speed)
				GPIO.output(self.pin,1)
				time.sleep(0.5/speed)
				system('clear')
		else:
			pass	

L1 = lights("white", 21)
L2 = lights("yellow", 16)
L3 = lights("red", 12)
L4 = lights("blue", 25)
L5 = lights("green", 24)
L6 = lights("snow", 23)

while 1:
    for i in [L1,L2,L3,L4,L5,L6]:
        lights.toggle_switch(i)
        input()
