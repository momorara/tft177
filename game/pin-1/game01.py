"""
ピンは1側で固定
"""

import pigpio
from gpiozero import Button, PWMLED, DigitalOutputDevice
from PIL import Image, ImageDraw, ImageFont
import time
import random

# ===== ピン設定 =====
DC_PIN = 0
RESET_PIN = 18
BACKLIGHT_PIN = 13

SPI_DEVICE = 0
SPI_SPEED_HZ = 4000000

# ===== 入力（左右入れ替え）=====
SW_1 = Button(5, pull_up=False)
SW_2 = Button(6, pull_up=False)

# ===== バックライト =====
backlight = PWMLED(BACKLIGHT_PIN)
backlight.value = 1.0

# ===== pigpio SPI =====
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

# ===== SPI関数 =====
def send_command(cmd):
    dc.off()
    pi.spi_xfer(spi, [cmd])

def send_data(data):
    dc.on()
    for i in range(0, len(data), 4096):
        pi.spi_xfer(spi, data[i:i+4096])

def reset_display():
    reset.off()
    time.sleep(0.1)
    reset.on()
    time.sleep(0.1)

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

def draw_image():
    dsp = image.rotate(180)

    send_command(0x2A)
    send_data([0, 0, 0, width - 1])
    send_command(0x2B)
    send_data([0, 0, 0, height - 1])
    send_command(0x2C)

    px = dsp.load()
    data = []
    for y in range(height):
        for x in range(width):
            r, g, b = px[x, y]
            c = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            data.append((c >> 8) & 0xFF)
            data.append(c & 0xFF)

    send_data(data)

# ===== 初期化 =====
init_display()

# ===== プレイヤー =====
player_w, player_h = 10, 10
player_x = width // 2
player_y = height - 20

# ===== 色候補 =====
COLORS = ["red", "yellow", "green", "white"]

# ===== 敵（サイズ＋色＋速度ランダム）=====
def create_enemy():
    size = random.choice([6, 8, 10, 14, 18])
    return {
        "x": random.randint(0, width - size),
        "y": 0,
        "w": size,
        "h": size,
        "speed": random.randint(3, 6),
        "color": random.choice(COLORS)  # ←追加
    }

enemies = [create_enemy()]

# ===== 状態 =====
score = 0
game_over = False
font = ImageFont.load_default()

# ===== 衝突判定 =====
def check_collision():
    for e in enemies:
        if (
            player_x < e["x"] + e["w"] and
            player_x + player_w > e["x"] and
            player_y < e["y"] + e["h"] and
            player_y + player_h > e["y"]
        ):
            return True
    return False

# ===== メインループ =====
try:
    while not game_over:

        # ===== 入力（左右逆）=====
        if SW_1.is_pressed:
            player_x = min(width - player_w, player_x + 5)
        if SW_2.is_pressed:
            player_x = max(0, player_x - 5)

        # ===== 敵移動 =====
        for e in enemies:
            e["y"] += e["speed"]

            if e["y"] > height:
                e.update(create_enemy())
                score += 1

        # ===== 敵追加（5点ごと）=====
        if score > 0 and score % 5 == 0:
            if len(enemies) < (score // 5) + 1:
                enemies.append(create_enemy())

        # ===== 衝突 =====
        if check_collision():
            game_over = True

        # ===== 描画 =====
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, width, height), fill="black")

        # プレイヤー
        draw.rectangle((player_x, player_y,
                        player_x + player_w, player_y + player_h),
                       fill="blue")

        # 敵（色付き）
        for e in enemies:
            draw.rectangle((e["x"], e["y"],
                            e["x"] + e["w"], e["y"] + e["h"]),
                           fill=e["color"])

        draw.text((5, 5), f"Score: {score}", fill="white", font=font)

        draw_image()
        time.sleep(0.05)

    # ===== GAME OVER =====
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), fill="black")
    draw.text((30, 50), "GAME OVER", fill="white", font=font)
    draw.text((30, 70), f"Score: {score}", fill="white", font=font)

    draw_image()
    time.sleep(5)

except KeyboardInterrupt:
    pass

finally:
    pi.spi_close(spi)
    pi.stop()