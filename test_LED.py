
#!/usr/bin/python

"""
###########################################################################
# LEDを on off

#Filename      :test_LED.py
#Description   :blink LED

LEDを点滅させます。

#Update        :2019/11/02

scp -r GPIO pi@192.168.68.128:/home/tk/
############################################################################
"""

import RPi.GPIO as GPIO

import time

# set GPIO 0 as LED pin
LEDPIN = 17
LEDPIN2 = 27

#print message at the begining ---custom function
def print_message():
    print ('|********************************|')
    print ('|   blink LED 2パターン           |')
    print ('|********************************|\n')
    print ('Program is running...')
    print ('Please press Ctrl+C to end the program...')

#setup function for some setup---custom function
def setup():
    GPIO.setwarnings(False)
    #set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    #set LEDPIN's mode to output,and initial level to LOW(0V)
    GPIO.setup(LEDPIN,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(LEDPIN2,GPIO.OUT,initial=GPIO.LOW)

def LedUpDown(on_off):
    j = int(10 / (on_off + 0.5))
    for i in range(j):
        GPIO.output(LEDPIN,GPIO.HIGH)
        time.sleep(on_off)
        GPIO.output(LEDPIN,GPIO.LOW)
        time.sleep(0.5)

def LedUpDown2(on_off):
    j = int(10 / (on_off + 0.5))
    for i in range(j):
        GPIO.output(LEDPIN2,GPIO.HIGH)
        time.sleep(on_off)
        GPIO.output(LEDPIN2,GPIO.LOW)
        time.sleep(0.5)

#main function
def main():
    #print info
    print_message()
    while True:
       LedUpDown(0.5)
       LedUpDown(1.0)

       time.sleep(0.5)

       LedUpDown2(0.5)
       LedUpDown2(1.0)
    pass

#define a destroy function for clean up everything after the script finished
def destroy():
    #turn off LED
    GPIO.output(LEDPIN,GPIO.LOW)
    #release resource
    GPIO.cleanup()
#
# if run this script directly ,do:
if __name__ == '__main__':
    setup()
    try:
            main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        destroy()

   
