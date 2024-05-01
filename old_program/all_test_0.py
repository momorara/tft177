
#!/usr/bin/python

"""
###########################################################################
一連のテストを連続して実行
2023/08/19
2024/02/10  ターミナルプロックの位置に対応するプログラムの整理
############################################################################
"""

import RPi.GPIO as GPIO
import time
import lcd177_0
import test_sw
from PIL import Image, ImageDraw, ImageFont

lcd177_0.init('on')
mes= '12345678901234567890123456'
print(mes)
lcd177_0.disp(mes,12,'white')
mes= '12345678901234567890'
lcd177_0.disp(mes,16,'blue')
mes= '1234567890123456'
lcd177_0.disp(mes,20,'red')
mes= '1234567890123'
lcd177_0.disp(mes,24,'green')
mes= '12345678901'
lcd177_0.disp(mes,28,'white')
mes= '12345678901'
lcd177_0.disp(mes,32,'blue')
time.sleep(0.5)
lcd177_0.init('reset')

lcd177_0.init('on')
mes= 'abcdefghijklmnopqrstuvqxyz'
print(mes)
lcd177_0.disp(mes,12,'white')
mes= 'abcdefghijklmnopqrst'
lcd177_0.disp(mes,16,'blue')
mes= 'abcdefghijklmnop'
lcd177_0.disp(mes,20,'red')
mes= 'abcdefghijklm'
lcd177_0.disp(mes,24,'green')
mes= 'abcdefghijk'
lcd177_0.disp(mes,28,'white')
time.sleep(0.5)
lcd177_0.init('reset')

lcd177_0.init('on')
print('abcdefghijklmnopqrstuvqxyz')
mes= '本日は晴天なり本日は晴天な'
lcd177_0.disp(mes,12,'white')
print('12345678901234567890')
mes= '本日は晴天なり本日は'
lcd177_0.disp(mes,16,'blue')
print('1234567890123456')
mes= '本日は晴天なり本り'
lcd177_0.disp(mes,20,'red')
print('1234567890123')
mes= '本日は晴天な'
lcd177_0.disp(mes,24,'green')
print('12345678901')
mes= '本日は晴天'
lcd177_0.disp(mes,28,'white')
time.sleep(0.5)
lcd177_0.init('reset')

for i in range(1,8):
    dsp_file = "/home/pi/tft177/photo/ph_" + str(i) + ".JPG"
    lcd177_0.dsp_file(dsp_file)
    time.sleep(0.5)
    lcd177_0.init('reset')    
lcd177_0.init('off')


# set GPIO 0 as LED pin
LEDPIN = 17
LEDPIN2 = 27
# set GPIO 0 as switch pin
SW_PIN_1 = 5
SW_PIN_2 = 6

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
    GPIO.setup(SW_PIN_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
    GPIO.setup(SW_PIN_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

def LedUpDown(on_off):
    j = 3
    for i in range(j):
        GPIO.output(LEDPIN,GPIO.HIGH)
        time.sleep(on_off)
        GPIO.output(LEDPIN,GPIO.LOW)
        time.sleep(0.5)

def LedUpDown2(on_off):
    j = 3
    for i in range(j):
        GPIO.output(LEDPIN2,GPIO.HIGH)
        time.sleep(on_off)
        GPIO.output(LEDPIN2,GPIO.LOW)
        time.sleep(0.5)

#main function
def main():
    #print info
    print('LED test')

    lcd177_0.init('on')
    mes= ' '
    lcd177_0.disp(mes,36,'white')
    mes= 'LED Test'
    lcd177_0.disp(mes,36,'white')

    LedUpDown(0.2)
    time.sleep(0.2)
    LedUpDown2(0.2)

    lcd177_0.init('reset')

    lcd177_0.init('on')
    mes= ' '
    lcd177_0.disp(mes,36,'white')
    mes= 'SW Test'
    lcd177_0.disp(mes,36,'white')

    loop_n = 0
    #print info
    sw_ = 'off'
    print()
    print('LED sw')
    while True:
        sw_ = test_sw.ReadSW_1()
        if sw_ =='off':
            print('sw_1_off')
        else:
            print('sw_1_on')
        time.sleep(1)

        sw_ = test_sw.ReadSW_2()
        if sw_ =='off':
            print('sw_2_off')
        else:
            print('sw_2_on')
        time.sleep(1)
    pass


#define a destroy function for clean up everything after the script finished
def destroy():
    lcd177_0.init('reset')
    lcd177_0.init('off')
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

   
