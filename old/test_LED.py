
#!/usr/bin/python

"""
###########################################################################
# LEDを on off

#Filename      :test_LED.py
#Description   :blink LED

LEDを点滅させます。

#Update        :2019/11/02

2025/01/07  pi5のためgpiozeroに置き換え


############################################################################
"""

from gpiozero import LED
import time

LEDPIN = LED(17)
LEDPIN2 = LED(27)

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

    LEDPIN .blink(on_time = 0.2, off_time = 0.2, n = 6, background = False)
    LEDPIN2.blink(on_time = 0.2, off_time = 0.2, n = 6, background = False)

if __name__ == '__main__':
    try:
        main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        pass
    except ValueError as e:
        print(e)