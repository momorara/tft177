
#!/usr/bin/python

"""
###########################################################################
# LEDを on off

#Filename      :test_LED.py
#Description   :blink LED

LEDを点滅させます。

#Update        :2019/11/02

2024/02/27  pi5のためgpiozeroに置き換え
2024/04/30  pi5仮想環境ではgpiozeroが使えなかったので、digitalioにて書き換え

scp -r GPIO pi@192.168.68.128:/home/tk/
############################################################################
"""

# from gpiozero import LED
# import time

# LEDPIN = LED(17)
# LEDPIN2 = LED(27)

import digitalio
import board
import time
LEDPIN     = digitalio.DigitalInOut(board.D17) 
LEDPIN.direction = digitalio.Direction.OUTPUT
LEDPIN.value = False  # Turn on the backlight

LEDPIN2     = digitalio.DigitalInOut(board.D27) 
LEDPIN2.direction = digitalio.Direction.OUTPUT
LEDPIN2.value = False  # Turn on the backlight
"""
LEDPIN.on()
time.sleep(2)
LEDPIN.off()

LEDPIN2.on()
time.sleep(2)
LEDPIN2.off()
"""

#print message at the begining ---custom function
def print_message():
    print ('|********************************|')
    print ('|   blink LED 2パターン           |')
    print ('|********************************|\n')
    print ('Program is running...')
    print ('Please press Ctrl+C to end the program...')


#main function
def main():
    #print info
    print_message()

    for _ in range(4):
        LEDPIN.value = True
        time.sleep(0.5)
        LEDPIN.value = False
        time.sleep(0.3)
    
    for _ in range(4):
        LEDPIN2.value = True
        time.sleep(0.5)
        LEDPIN2.value = False
        time.sleep(0.3)


    # LEDPIN .blink(on_time = 0.2, off_time = 0.2, n = 6, background = False)
    # LEDPIN2.blink(on_time = 0.2, off_time = 0.2, n = 6, background = False)


if __name__ == '__main__':
    main()
