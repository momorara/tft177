# MIT License
# Copyright (c) 2026 Takanobu Kawabata

import math
import time
import datetime as dt
from PIL import ImageDraw, ImageFont

import lcd177_0 as tft

# ===== 基本設定 =====
WIDTH = tft.width
HEIGHT = tft.height
CX = WIDTH // 2
CY = HEIGHT // 2
RAD = min(WIDTH, HEIGHT) // 2

# ===== フォント =====
# 大きい数字（約1.5倍）
font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
# 日付
font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)

# ===== 基本描画 =====
def line_angle(draw, deg, length, width, color):
    rad = math.radians(deg)
    x = math.sin(rad) * length
    y = -math.cos(rad) * length

    draw.line(
        (CX - x/5, CY - y/5, CX + x, CY + y),
        fill=color,
        width=int(width)
    )

def circle(draw, r, outline=None, fill=None, width=1):
    draw.ellipse(
        (CX-r, CY-r, CX+r, CY+r),
        outline=outline,
        fill=fill,
        width=width
    )

# ===== 数字（太字＋拡大） =====
def draw_numbers(draw):
    r = RAD * 0.65  # ← 大きくしたので少し内側へ
    nums = {"12":0, "3":90, "6":180, "9":270}

    for txt, deg in nums.items():
        rad = math.radians(deg)
        x = CX + math.sin(rad)*r
        y = CY - math.cos(rad)*r

        bbox = draw.textbbox((0,0), txt, font=font_big)
        w = bbox[2]-bbox[0]
        h = bbox[3]-bbox[1]

        px = x - w/2
        py = y - h/2 - 3

        # 疑似ボールド（軽め）
        for dx, dy in [(0,0),(1,0),(0,1)]:
            draw.text((px+dx, py+dy), txt, fill=(20,20,20), font=font_big)

# ===== 文字盤 =====
def draw_dial(draw):
    circle(draw, RAD*0.95, outline="gray", fill="white", width=2)

    for d in range(0, 360, 6):
        line_angle(draw, d, RAD*0.94, 1, "black")

    for d in range(0, 360, 30):
        line_angle(draw, d, RAD*0.90, 3, "black")

    circle(draw, RAD*0.85, fill="white")

    draw_numbers(draw)

# ===== 日付（ゼロサプレス＋太字） =====
def draw_date(draw, now):
    date_str = str(now.day)  # ← ゼロサプレス

    x = CX + RAD * 0.23   # ← 少し右
    y = CY - RAD * 0.05

    bbox = draw.textbbox((0,0), date_str, font=font_small)
    w = bbox[2]-bbox[0]
    h = bbox[3]-bbox[1]

    px = x - w/2
    py = y - h/2

    # 背景
    draw.rectangle(
        (px-3, py-3, px+w+3, py+h+3),
        fill="white"
    )

    # 太字（強め）
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(0,0)]:
        draw.text((px+dx, py+dy), date_str, fill=(20,20,20), font=font_small)

# ===== 初期化 =====
tft.init('reset')
tft.init('on')

# 文字盤を1回だけ描画（フラッシュ防止）
draw = ImageDraw.Draw(tft.image)
draw_dial(draw)
background = tft.image.copy()

# ===== メインループ =====
try:
    while True:
        tft.image.paste(background)

        draw = ImageDraw.Draw(tft.image)
        now = dt.datetime.now()

        # 日付
        draw_date(draw, now)

        # 針
        sec = (now.second + now.microsecond*1e-6) * 6
        minute = (now.minute + now.second/60) * 6
        hour = (now.hour % 12) * 30 + now.minute/2

        line_angle(draw, sec, RAD*0.83, 1, "red")
        line_angle(draw, minute, RAD*0.80, 3, "black")
        line_angle(draw, hour, RAD*0.60, 5, "black")

        # 中心
        circle(draw, RAD*0.05, fill="white", outline="black", width=2)

        # 表示
        tft.draw_image()

        time.sleep(0.05)

finally:
    tft.set_backlight(False)