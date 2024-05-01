#!/usr/bin/python

"""
###########################################################################
スイッチの状態を確認する。

#Filename      :test_sw.py

#Update        :2019/11/02
2023/9/22   タクトスイッチ　ソフトプルダウンとする。
2024/02/27  pi5のためgpiozeroに置き換え
2024/04/30  pi5仮想環境ではgpiozeroが使えなかったので、digitalioにて書き換え
############################################################################
"""
# from gpiozero import Button

import digitalio
import board
import time

# SW_1 = Button(5,pull_up=False)
# SW_2 = Button(6,pull_up=False)

SW_1           = digitalio.DigitalInOut(board.D5) 
SW_1.direction = digitalio.Direction.INPUT
SW_1.pull      = digitalio.Pull.DOWN
SW_2           = digitalio.DigitalInOut(board.D6) 
SW_2.direction = digitalio.Direction.INPUT
SW_2.pull      = digitalio.Pull.DOWN

#print message at the begining ---custom function
def print_message():
    print ('|********************************|')
    print ('|   switch 監視　　　　　          |')
    print ('|********************************|\n')
    print ('Program is running...')
    print ('Please press Ctrl+C to end the program...')

#read SW_PI_1's level
def ReadSW_1():
    pin_value = SW_1.value
    if pin_value == True:
        sw_ = 'on'
    else:
        sw_ = 'off'
    return sw_

#read SW_PI_2's level
def ReadSW_2():
    pin_value = SW_2.value
    if pin_value == True:
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

#
# if run this script directly ,do:
if __name__ == '__main__':
    try:
            main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        pass
    except ValueError as e:
        print(e)

   
