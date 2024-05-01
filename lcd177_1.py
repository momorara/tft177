# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Released under the MIT license
https://github.com/YukinobuKurata/YouTubeMagicBuyButton/blob/master/MIT-LICENSE.txt

This program is based on the sample program at Adafruit-Python-Usage.
This will show some Linux Statistics on the attached display. Be sure to adjust
to the display you have connected. Be sure to check the learn guides for more
usage information.

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!

2022/04/09  使いやすいように改変した
            日本語対応
2022/04/10  関数化してみる
    lcd177.pyとして関数化
    lcd177.init('on')     として表示開始 バックライト点灯
    lcd177.disp('message')として表示する
    lcd177.size(16)       としてフォントサイズ指定 デフォルト 12
    lcd177.color('green') として文字色指定 デフォルト 白 ,#0000FFも可能
    lcd177.init('off')    として表示終了 バックライト消灯
    lcd177.init('reset')  として液晶をリセット
    lcd177.disp('message',size,color)size指定、色指定も可能
                colorは white,blue,red,greenが使える
                        #0000FFといった指定も可能
    ただし、色、サイズ、messageのエラーチェックはしていないので、要チェック

            固定設定
            DISP_rotation:0,90,180,270で指定

2022/04/11  lcd177.image_f(画像ファイルパス)
2022/04/14  pin整理
2022/06/17  整理、関数名修正
2022/10/10  init('reset')にバグ 修正した。
2024/02/10  ターミナルプロックの位置に対応するプログラムの整理
2024/04/24  神山様からPi5用対処を頂いた
2024/04/29  font.getsizeでエラーになるのを回避
"""
import time
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import numpy as np

from time import sleep
#GPIOは消す(2024.04.24)
#import RPi.GPIO as GPIO
from adafruit_rgb_display import st7735  # pylint: disable=unused-import

reset = 24

# ターミナルプロックを液晶側に設定した場合を位置1
cs_pin        = digitalio.DigitalInOut(board.CE0)
dc_pin        = digitalio.DigitalInOut(board.D0) #RS/DC  25 or 0
reset_pin     = digitalio.DigitalInOut(board.D18)       # 24 or 18
#backlight pinの部分を変更 2024.04.24
#backlight_pin = 13                                      # 12 or 13


BAUDRATE      = 24000000
DISP_rotation = 270 # 0,90,180,270
FONTSIZE      = 12  # 9〜128 なら見える
FONTCOLOR     = "#FFFFFF"
# First define some constants to allow easy positioning of text.
disp_padding = -2
disp_y = -disp_padding
disp_x = 0


# 使用する液晶が異なる場合、サイトを参考に以下を書き換えてください。
# ----------ここから----------
disp_lcd_177 = st7735.ST7735R(
    board.SPI(),
    rotation=DISP_rotation,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)
# バックライト制御(削除2024.4.24)
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(backlight_pin, GPIO.OUT)
backlight_pin = digitalio.DigitalInOut(board.D13)  # Backlight control # 12 or 13
backlight_pin.direction = digitalio.Direction.OUTPUT
backlight_pin.value = True  # Turn on the backlight

# ----------ここまで----------

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if disp_lcd_177.rotation % 180 == 90:
    height = disp_lcd_177.width  # we swap height/width to rotate it to landscape!
    width = disp_lcd_177.height
else:
    width = disp_lcd_177.width  # we swap height/width to rotate it to landscape!
    height = disp_lcd_177.height
image = Image.new("RGB", (width, height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp_lcd_177.image(image)
# Load a TTF font. 
font = ImageFont.truetype("fonts-japanese-gothic.ttf", FONTSIZE)
# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)


def init(ini):
    # バックライト点灯
    if ini == 'on':
        #　バックライト変更(2024.4.24)
        backlight_pin.value = True
        #GPIO.output(backlight_pin,GPIO.HIGH)
        global FONTCOLOR
        FONTCOLOR = "#FFFFFF"
        # print('ini-on')

    # バックライト消灯
    if ini == 'off':
        #　バックライト変更(2024.4.24)
        backlight_pin.value = False
        #GPIO.output(backlight_pin,GPIO.LOW)
        # print('ini-off')

    # 画面リセット カーソルを原点に戻す
    if ini == 'reset':
        # 画面を消去
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        # カーソルを原点に戻す
        global disp_x,disp_y
        disp_y = -2
        disp_x = 0
        disp('    ',48)
        disp_y = -2
        disp_x = 0


#液晶を簡単にテスト(2024.4.24)
def disp_test():
    font_title = ImageFont.truetype("fonts-japanese-gothic.ttf", 15)
    
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    draw.text((30, 40), "starting test...", "white", font=font_title)
    draw.text((45, 60), "test raspi 5" , "white", font=font_title)
    disp_lcd_177.image(image)    

def disp(mes,size=1,color='no'):
    # サイズ、色を指定してdispを呼んだ場合は、その指定に従い
    # mesのみ指定して呼んだ場合は、前回のサイズ、色に従う
    global font
    global font_size
    font_bak = font
    # 明示的にフォントサイズを指定されない場合は、直近で使ったフォントサイズを使用
    if size != 1:
        font = ImageFont.truetype("fonts-japanese-gothic.ttf", size)
        font_size = size

    global FONTCOLOR
    FONTCOLOR_bak = FONTCOLOR
    if color == 'white':
        color = "#FFFFFF"
    if color == 'red':
        color = "#0000FF"
    if color == 'blue':
        color = "#FF0000"
    if color == 'green':
        color = "#00FF00"
    if color == 'no':
        FONTCOLOR = FONTCOLOR_bak # 色指定が無い場合は、前回設定を使用
    else:
        FONTCOLOR = color

    global disp_x,disp_y
    draw.text((disp_x, disp_y), mes,  font=font, fill=FONTCOLOR)
    disp_lcd_177.image(image)
    # 使っているフォントサイズを取得できていたのに、出来なくてエラーになる。
    # global変数としてフォントサイズを持つようにする font_size 
    # disp_y += font.getsize(mes)[1]
    disp_y += font_size
    
    FONTCOLOR = FONTCOLOR_bak
    font = font_bak
    # print('tft')

def size(size):
    global font
    global font_size
    font = ImageFont.truetype("fonts-japanese-gothic.ttf", size)
    font_size = size

def color(color):
    if color == 'white':
        color = "#FFFFFF"
    if color == 'red':
        color = "#0000FF"
    if color == 'blue':
        color = "#FF0000"
    if color == 'green':
        color = "#00FF00"
    global FONTCOLOR
    FONTCOLOR = color

# 受け取ったファイルを液晶に表示
def dsp_file(file):
    # 受け取ったファイルからフレームを取り出し
    image = Image.open(file)
    # dsp_frameに渡す
    dsp_frame(image)

# 受け取ったフレームを液晶に表示
def dsp_frame(frame):
    # まず、液晶を白紙状態にします。
    # Make sure to create image with mode 'RGB' for full color.
    if disp_lcd_177.rotation % 180 == 90 :
        height = disp_lcd_177.width  # we swap height/width to rotate it to landscape!
        width  = disp_lcd_177.height
    else:
        width = disp_lcd_177.width  # we swap height/width to rotate it to landscape!
        height = disp_lcd_177.height
    image = Image.new("RGB", (width, height))
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp_lcd_177.image(image)

    # 描画すべき画像データのパスを渡します。
    # 読み込む画像データがRGBで、液晶はGBRなので色変換が必要
    # image = Image.open(dsp_file)
    # Pillow -> NumPyへの変換
    image_np = np.array(frame)
    # RGBからGBRへ変換
    image_np = image_np[:, :, ::-1]
    # NumPy -> Pillowへの変換
    image = Image.fromarray(image_np)

    # 画像データの大きさを調整します。
    # Scale the image to the smaller screen dimension
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)
    # Crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))

    # 画像データを表示します。
    disp_lcd_177.image(image)

def main():

    #ディスプレイの簡単なテスト(2024.4.24)
    disp_test()

    time.sleep(5)

    init('on')
    init('reset')

''' フォントでエラーが出る(2024.4.24)
    print('1')
    init('on')
    init('reset')
    size(24)

    mes= '本プログラムはライブラリ集です'
    color('white')
    disp(mes)
    time.sleep(0.4)
    mes= 'testプログラムは'
    color('red')
    disp(mes)
    time.sleep(0.4)
    mes= 'このライブラリを使って'
    color('red')
    disp(mes)
    time.sleep(0.4)
    mes= '表示しています。'
    color('red')
    disp(mes)

    time.sleep(3)
    init('reset')
    init('off')
'''
 
    # print('1')
    # init('on')
    # init('reset')

    # file = "./photo/ph_3.JPG"
    # print('2')
    # dsp_file(file)
    # time.sleep(1)
    # # exit(0)

    # mes= 'red'
    # color('red')
    # disp(mes)
    # time.sleep(1)

    # mes= 'white'
    # color('white')
    # size(24)
    # disp(mes)
    # time.sleep(1)

    # mes= 'green'
    # color('green')
    # size(36)
    # disp(mes)
    # time.sleep(1)

    # mes= 'blue'
    # color('blue')
    # size(48)
    # disp(mes)
    # time.sleep(1)

    # file = "./photo/ph_2.JPG"
    # dsp_file(file)    
    # time.sleep(2)

    # init('reset')
    # init('off')


if __name__ == "__main__":
    main()
