#!/usr/bin/python
# -*- coding: utf-8 -*-

"By Andre Akue"

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)
import time
import datetime
from os import system
from multiprocessing import Process

speed = 2 #blinking speed
day_duration = 60*60*24
check_time = 600 #check for day change every 600 secs

class lights: #setting up leds

    def __init__(self,color_name,color_pin):
        self.name = color_name
        self.pin = color_pin
        GPIO.setup(self.pin, GPIO.OUT, initial = 0)
        
    def solid(self):
        GPIO.output(self.pin,1)
        time.sleep(check_time)
        GPIO.output(self.pin,0)
        
    def flash(self): #blink
        stp = time.time() ; etp = time.time() + check_time # stp/etp = starting / ending time pattern
        while time.time() < etp:
            GPIO.output(self.pin,0)
            time.sleep(0.8/speed)
            GPIO.output(self.pin,1)
            time.sleep(0.2/speed)
            GPIO.output(self.pin,0)

L1 = lights("white", 21)
L2 = lights("yellow", 16)
L3 = lights("red", 12)
L4 = lights("blue", 25)
L5 = lights("green", 24)
L6 = lights("snow", 23)

def chores():#a 6 day cycle divided into 3 steps of 2 days each
    while 1:
    #Sweeping the floor - First Day
        L2.solid()#yellow stays on
    #Sweeping the floor - Second Day
        L2.flash()#yellow keeps blinking
    #Setting the table - First Day
        L3.solid()#red stays on
    #Setting the table - Second Day
        L3.flash()#red keeps blinking
    #Washing dishes - First Day
        GPIO.output((L2.pin,L3.pin),1)#red and yellow stay on
        time.sleep(check_time)
        GPIO.output((L2.pin,L3.pin),0)
    #Washing dishes - Second Day
        stp = time.time() ; etp = time.time() + check_time # stp/etp = starting / ending time pattern
        while time.time() < etp:#red and yellow keep blinking
            GPIO.output((L2.pin,L3.pin),0)
            time.sleep(0.8/speed)
            GPIO.output((L2.pin,L3.pin),1)
            time.sleep(0.2/speed)
            GPIO.output((L2.pin,L3.pin),0)

def log():# print weekday and day count in command prompt
    count = 0
    while 1:
        for day in week_order:
            count += 1
            print ('\nDay: %s\t\tDay of the week: %i' % (day,count))
            time.sleep(day_duration)

def vacumm():
    while 1:
    #only happens friday to sunday every 3 weeks
        for day in list(range(1,22)):
            if day not in [4,5,6]:
                time.sleep(day_duration)
            elif day == 4:
                L5.solid()
            elif day == 5:
                L5.solid()
            elif day == 6:
                L5.flash()



def start_tomorrow(): #cycle starts the day after the code has been started
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    while datetime.datetime.now() < tomorrow:
        time.sleep(60)
        print ('\nchore cycle started')

def fixed(): #all weekly, fixed items
    while 1:
        if datetime.datetime.now().strftime('%a') == 'Mon':
            L1.flash()#trash
            L6.solid()#recycle
        elif datetime.datetime.now().strftime('%a') == 'Tue':
            L6.flash()#recycle
        elif datetime.datetime.now().strftime('%a') == 'Wed':
            L1.solid()#trash
            L4.solid()#bath
        elif datetime.datetime.now().strftime('%a') == 'Thu':
            L1.flash()#trash
            L4.flash()#bath
        elif datetime.datetime.now().strftime('%a') == 'Fri':
            
        elif datetime.datetime.now().strftime('%a') == 'Sat':
            
        elif datetime.datetime.now().strftime('%a') == 'Sun':
            L1.solid()#trash

try:#using processes so that different cycles can run independently
    if __name__ == '__main__':
        Process(target=log).start()
        Process(target=chores).start()
        Process(target=bath).start()
        Process(target=recycle).start()
        Process(target=vacumm).start()
        Process(target=trash).start()

except KeyboardInterrupt:
    system('clear')
    print ("\n\n\texited via keyboard interrupt\n\n")
    GPIO.cleanup()

#when resetting:
#3-chore cycle
#   place the chore happenning tomorrow in first place in the sequence

#'bath','trash','recycle', and 'log'
#   place the day of tomorrow in first in the list of weekdays
#   'week_order'

#vaccum cycle
#   count the number of days till the next 'first vaccum day',
#   and start with this number in the list of the "if" loops
