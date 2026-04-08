"""
2025/01/08 独自にspi通信で表示制御する
2025/01/09
    imageを引数にすると面倒なので、グローバルにする
    なるべく元の関数に近づける 
    仮想環境を使わなくても動作する。

2026/04/08 spidevを使わずにpigpioで書き換え
"""
print("pigpio")
import pigpio
from gpiozero import DigitalOutputDevice
from PIL import Image, ImageDraw, ImageFont
import time

# ピン設定
CS_PIN = 0  # CE0
DC_PIN = 0
RESET_PIN = 18
BACKLIGHT_PIN = 13

# SPI設定
SPI_BUS = 0
SPI_DEVICE = 0
SPI_SPEED_HZ = 4000000  # pigpioは4〜8MHz推奨

# GPIO設定
dc = DigitalOutputDevice(DC_PIN)
reset = DigitalOutputDevice(RESET_PIN)
backlight = DigitalOutputDevice(BACKLIGHT_PIN)

# ===== SPI初期化（spidev → pigpio）=====
pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("pigpio daemon not running (sudo pigpiod)")

spi = pi.spi_open(SPI_DEVICE, SPI_SPEED_HZ, 0)

width=160
height=128
disp_padding = -2
disp_y = -disp_padding
disp_x = 0
image = Image.new("RGB", (width, height), "black")
FONTSIZE      = 12
FONTCOLOR     = "white"
font = ImageFont.truetype("fonts-japanese-gothic.ttf", FONTSIZE)

# コマンド送信
def send_command(cmd):
    dc.off()
    pi.spi_xfer(spi, [cmd])

# データ送信（チャンク処理付き）
def send_data(data):
    dc.on()
    chunk_size = 4096
    for i in range(0, len(data), chunk_size):
        pi.spi_xfer(spi, data[i:i+chunk_size])

# リセット関数
def reset_display():
    reset.off()
    time.sleep(0.1)
    reset.on()
    time.sleep(0.1)

# 初期化関数
def init_display():
    reset_display()
    send_command(0x01)
    time.sleep(0.15)
    send_command(0x11)
    time.sleep(0.12)
    send_command(0x3A)
    send_data([0x05])
    send_command(0x36)
    send_data([0x70])
    send_command(0x29)
    time.sleep(0.1)

# バックライト制御
def set_backlight(state):
    if state:
        backlight.on()
    else:
        backlight.off()

# 画像描画
def draw_image():
    dsp_image = image.rotate(180)

    width, height = dsp_image.size
    send_command(0x2A)
    send_data([0x00, 0, 0x00, width - 1])
    send_command(0x2B)
    send_data([0x00, 0, 0x00, height - 1])
    send_command(0x2C)

    pixels = dsp_image.convert("RGB").load()
    pixel_data = []
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            color = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            pixel_data.append((color >> 8) & 0xFF)
            pixel_data.append(color & 0xFF)
    send_data(pixel_data)

def init(ini):
    global image
    global disp_x,disp_y

    if ini == 'on':
        backlight.on()
        ini = 'reset'

    if ini == 'off':
        backlight.off()

    if ini == 'reset':
        init_display()
        image = Image.new("RGB", (width, height), "black")
        draw_image()
        disp_y = -2
        disp_x = 0
        disp_y = -2
        disp_x = 0

# テキスト描画
def draw_text(text):
    global FONTCOLOR
    global FONTSIZE
    global disp_x
    global disp_y
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("fonts-japanese-gothic.ttf", FONTSIZE)

    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    draw.text((disp_x, disp_y), text, font=font, fill=FONTCOLOR)

# ピクセル描画
def pixel(x, y, color):
    draw = ImageDraw.Draw(image)
    draw.point((x, y), fill=color)

# image領域を黒で塗りつぶして表示し返す
def imageClear():
    global image
    global disp_x,disp_y
    disp_y = -disp_padding
    disp_x = 0
    image = Image.new("RGB", (width, height), "black")
    draw_image()

def size(size):
    global FONTSIZE
    FONTSIZE = size

def color(color):
    global FONTCOLOR
    FONTCOLOR = color

def disp(mes,size=1,color='no'):
    global FONTSIZE
    global FONTCOLOR
    global disp_x,disp_y

    if size != 1:
        font = ImageFont.truetype("fonts-japanese-gothic.ttf", size)
        FONTSIZE = size

    if color != 'no':
        FONTCOLOR = color

    draw_text(mes)
    disp_y = disp_y + FONTSIZE
    draw_image()

# JPEGファイルを描画する関数
def dsp_file(file_name):
    try:
        global image
        img = Image.open(file_name)

        if hasattr(Image, "Resampling"):
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        else:
            img = img.resize((width, height), Image.ANTIALIAS)

        image = img
        draw_image()

    except FileNotFoundError:
        print(f"エラー: {file_name} が見つかりません。")
    except Exception as e:
        print(f"エラー: {str(e)}")

# ===== メイン処理（完全に元のまま）=====
if __name__ == "__main__":

    try:
        print("Initializing display...")
        init('reset')
        init('on')

        mes= 'テストです。'
        color('red')
        size(16)
        print(FONTCOLOR,FONTSIZE)
        disp(mes)

        time.sleep(2)
        color('white')
        size(26)
        print(FONTCOLOR,FONTSIZE)
        disp(mes)
        color('red')        
        disp(mes)
        color('blue')
        disp(mes)

        print("Text drawn!")

        time.sleep(2)
        imageClear()
        color('green')
        disp(mes)
        time.sleep(3)

        file_name = "photo/ph_1.JPG"
        dsp_file(file_name)
        time.sleep(3)
        
        init('off')
        init('reset')
        
    finally:
        print("Turning off backlight.")
        set_backlight(False)
        pi.spi_close(spi)
        pi.stop()