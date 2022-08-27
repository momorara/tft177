#!/usr/bin/python

"""
###########################################################################
スイッチの状態を確認する。

#Filename      :test_sw.py

#Update        :2019/11/02
############################################################################
"""

import RPi.GPIO as GPIO
import time

# set GPIO 0 as switch pin
SW_PIN_1 = 5
SW_PIN_2 = 6

#print message at the begining ---custom function
def print_message():
    print ('|********************************|')
    print ('|   switch 監視　　　　　          |')
    print ('|********************************|\n')
    print ('Program is running...')
    print ('Please press Ctrl+C to end the program...')

#setup function for some setup---custom function
def setup():
    GPIO.setwarnings(False)
    #set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SW_PIN_1,GPIO.IN)
    GPIO.setup(SW_PIN_2,GPIO.IN)

#read SW_PI_1's level
def ReadSW_1():
    if (GPIO.input(SW_PIN_1)):
        sw_ = 'on'
    else:
        sw_ = 'off'
    return sw_

#read SW_PI_2's level
def ReadSW_2():
    if (GPIO.input(SW_PIN_2)):
        sw_ = 'on'
    else:
        sw_ = 'off'
    return sw_

#main function
def main():
    loop_n = 0
    #print info
    sw_ = 'off'
    print_message()
    while True:
        sw_ = ReadSW_1()
        if sw_ =='off':
            print('sw_1_off')
            
        else:
            print('sw_1_on')
        time.sleep(1)

        sw_ = ReadSW_2()
        if sw_ =='off':
            print('sw_2_off')
            
        else:
            print('sw_2_on')
        time.sleep(1)
    pass

#define a destroy function for clean up everything after the script finished
def destroy():
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
    except ValueError as e:
        print(e)

   
