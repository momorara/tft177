"""
ピンは1側で固定
"""

import pigpio
from gpiozero import Button, PWMLED, DigitalOutputDevice
from PIL import Image, ImageDraw, ImageFont
import time
import random

# ===== ピン =====
DC_PIN = 0
RESET_PIN = 18
BACKLIGHT_PIN = 13

SPI_DEVICE = 0
SPI_SPEED_HZ = 4000000

# ===== 入力（左右逆）=====
SW_1 = Button(5, pull_up=False)
SW_2 = Button(6, pull_up=False)

# ===== バックライト =====
backlight = PWMLED(BACKLIGHT_PIN)
backlight.value = 1.0

# ===== SPI =====
pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("pigpio daemon not running")

spi = pi.spi_open(SPI_DEVICE, SPI_SPEED_HZ, 0)

dc = DigitalOutputDevice(DC_PIN)
reset = DigitalOutputDevice(RESET_PIN)

# ===== 画面 =====
width = 160
height = 128
image = Image.new("RGB", (width, height), "black")

# ===== SPI描画 =====
def send_command(cmd):
    dc.off()
    pi.spi_xfer(spi, [cmd])

def send_data(data):
    dc.on()
    for i in range(0, len(data), 4096):
        pi.spi_xfer(spi, data[i:i+4096])

def init_display():
    reset.off(); time.sleep(0.1)
    reset.on(); time.sleep(0.1)
    send_command(0x01); time.sleep(0.15)
    send_command(0x11); time.sleep(0.12)
    send_command(0x3A); send_data([0x05])
    send_command(0x36); send_data([0x70])
    send_command(0x29)

def draw_image():
    dsp = image.rotate(180)
    send_command(0x2A); send_data([0,0,0,width-1])
    send_command(0x2B); send_data([0,0,0,height-1])
    send_command(0x2C)

    px = dsp.load()
    data = []
    for y in range(height):
        for x in range(width):
            r,g,b = px[x,y]
            c = ((r & 0xF8)<<8)|((g & 0xFC)<<3)|(b>>3)
            data.append((c>>8)&0xFF)
            data.append(c&0xFF)
    send_data(data)

init_display()

# ===== 色 =====
COLORS = ["red", "yellow", "green", "white"]

# ===== パドル =====
paddle_w = 30
paddle_h = 5
paddle_x = width // 2 - paddle_w // 2
paddle_y = height - 10

# ===== ボール =====
ball_x = width // 2
ball_y = height // 2
ball_dx = 2
ball_dy = -2
ball_size = 4

# ===== ブロック =====
block_rows = 4
block_cols = 8
block_w = width // block_cols
block_h = 10

blocks = []
for row in range(block_rows):
    for col in range(block_cols):
        blocks.append({
            "x": col * block_w,
            "y": row * block_h,
            "w": block_w - 2,
            "h": block_h - 2,
            "color": random.choice(COLORS),
            "alive": True
        })

score = 0
game_over = False
font = ImageFont.load_default()

# ===== メイン =====
try:
    while not game_over:

        # ===== 入力（左右逆）=====
        if SW_1.is_pressed:
            paddle_x = min(width - paddle_w, paddle_x + 4)
        if SW_2.is_pressed:
            paddle_x = max(0, paddle_x - 4)

        # ===== ボール移動 =====
        ball_x += ball_dx
        ball_y += ball_dy

        # 壁反射
        if ball_x <= 0 or ball_x >= width - ball_size:
            ball_dx *= -1
        if ball_y <= 0:
            ball_dy *= -1

        # パドル反射
        if (paddle_y <= ball_y + ball_size <= paddle_y + paddle_h and
            paddle_x <= ball_x <= paddle_x + paddle_w):
            ball_dy *= -1

        # 落下
        if ball_y > height:
            game_over = True

        # ===== ブロック衝突 =====
        for b in blocks:
            if b["alive"]:
                if (ball_x < b["x"] + b["w"] and
                    ball_x + ball_size > b["x"] and
                    ball_y < b["y"] + b["h"] and
                    ball_y + ball_size > b["y"]):

                    b["alive"] = False
                    ball_dy *= -1
                    score += 1
                    break

        # ===== 描画 =====
        draw = ImageDraw.Draw(image)
        draw.rectangle((0,0,width,height), fill="black")

        # パドル
        draw.rectangle((paddle_x, paddle_y,
                        paddle_x + paddle_w, paddle_y + paddle_h),
                       fill="white")

        # ボール
        draw.rectangle((ball_x, ball_y,
                        ball_x + ball_size, ball_y + ball_size),
                       fill="yellow")

        # ブロック
        for b in blocks:
            if b["alive"]:
                draw.rectangle((b["x"], b["y"],
                                b["x"] + b["w"], b["y"] + b["h"]),
                               fill=b["color"])

        draw.text((5, 5), f"Score: {score}", fill="white", font=font)

        draw_image()
        time.sleep(0.03)

    # ===== GAME OVER =====
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), fill="black")
    draw.text((30,50), "GAME OVER", fill="white", font=font)
    draw.text((30,70), f"Score: {score}", fill="white", font=font)
    draw_image()
    time.sleep(5)

except KeyboardInterrupt:
    pass

finally:
    pi.spi_close(spi)
    pi.stop()