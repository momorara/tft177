import pigpio
from PIL import Image, ImageDraw
import time
import random
import math

# ===== TFT設定 =====
WIDTH_PX = 160
HEIGHT_PX = 128

CELL_SIZE = 4
WIDTH = WIDTH_PX // CELL_SIZE
HEIGHT = HEIGHT_PX // CELL_SIZE

RESTART_TIME = 120

DC_PIN = 25
RESET_PIN = 24
BACKLIGHT_PIN = 12   # ★追加

SPI_DEVICE = 0
SPI_SPEED_HZ = 4000000

# ===== pigpio初期化 =====
pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("pigpio daemon not running")

spi = pi.spi_open(SPI_DEVICE, SPI_SPEED_HZ, 0)

# GPIO設定（全部pigpio）
pi.set_mode(DC_PIN, pigpio.OUTPUT)
pi.set_mode(RESET_PIN, pigpio.OUTPUT)
pi.set_mode(BACKLIGHT_PIN, pigpio.OUTPUT)   # ★追加

pi.write(BACKLIGHT_PIN, 1)   # ★バックライトON

image = Image.new("RGB", (WIDTH_PX, HEIGHT_PX), "black")

# ===== SPI送信 =====
def send_command(cmd):
    pi.write(DC_PIN, 0)
    pi.spi_xfer(spi, [cmd])

def send_data(data):
    pi.write(DC_PIN, 1)
    for i in range(0, len(data), 4096):
        pi.spi_xfer(spi, data[i:i+4096])

# ===== 初期化 =====
def init_display():
    pi.write(RESET_PIN, 0)
    time.sleep(0.1)
    pi.write(RESET_PIN, 1)
    time.sleep(0.1)

    send_command(0x01)
    time.sleep(0.15)

    send_command(0x11)
    time.sleep(0.12)

    send_command(0x3A)
    send_data([0x05])

    send_command(0x36)
    send_data([0x70])

    send_command(0x29)

# ===== 描画 =====
def draw_image():
    dsp = image.rotate(180)

    send_command(0x2A)
    send_data([0,0,0,WIDTH_PX-1])

    send_command(0x2B)
    send_data([0,0,0,HEIGHT_PX-1])

    send_command(0x2C)

    px = dsp.load()
    buf = bytearray(WIDTH_PX * HEIGHT_PX * 2)

    i = 0
    for y in range(HEIGHT_PX):
        for x in range(WIDTH_PX):
            r,g,b = px[x,y]
            c = ((r & 0xF8)<<8)|((g & 0xFC)<<3)|(b>>3)
            buf[i] = (c>>8)&0xFF
            buf[i+1] = c&0xFF
            i += 2

    send_data(buf)

init_display()

# ===== ゲームロジック =====
grid = [[0]*WIDTH for _ in range(HEIGHT)]

start_time = time.time()
boost1_done = False
boost2_done = False
bigbang = False
bigbang_time = 0

def randomize():
    global start_time, boost1_done, boost2_done, bigbang
    for y in range(HEIGHT):
        for x in range(WIDTH):
            grid[y][x] = 1 if random.random() < 0.2 else 0
    start_time = time.time()
    boost1_done = False
    boost2_done = False
    bigbang = False

def count_neighbors(x, y):
    cnt = 0
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            if dx==0 and dy==0: continue
            nx = (x+dx)%WIDTH
            ny = (y+dy)%HEIGHT
            if grid[ny][nx] > 0:
                cnt += 1
    return cnt

def add_cells():
    for _ in range(random.randint(3,4)):
        grid[random.randint(0,HEIGHT-1)][random.randint(0,WIDTH-1)] = 1

def get_birth_prob(elapsed):
    if elapsed < 50: return 1.0
    if elapsed < 100: return 1.0 - (elapsed-50)/50
    return 0.02

def move_center():
    cx, cy = WIDTH//2, HEIGHT//2
    new = [[0]*WIDTH for _ in range(HEIGHT)]

    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[y][x]:
                dx = cx-x
                dy = cy-y
                dist2 = dx*dx + dy*dy + 0.1
                inv = 1/math.sqrt(dist2)

                nx = int(x + dx*inv*0.5)
                ny = int(y + dy*inv*0.5)

                nx = max(0,min(WIDTH-1,nx))
                ny = max(0,min(HEIGHT-1,ny))

                new[ny][nx] = grid[y][x]

    return new

def is_centered():
    cx, cy = WIDTH//2, HEIGHT//2
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[y][x]:
                if abs(x-cx)>2 or abs(y-cy)>2:
                    return False
    return True

def get_color(age):
    hue = (age*6)%360
    r = int(127*(1+math.sin(math.radians(hue))))
    g = int(127*(1+math.sin(math.radians(hue+120))))
    b = int(127*(1+math.sin(math.radians(hue+240))))
    return (r,g,b)

def draw(draw):
    draw.rectangle((0,0,WIDTH_PX,HEIGHT_PX), fill="black")
    alive = 0

    for y in range(HEIGHT):
        for x in range(WIDTH):
            age = grid[y][x]
            if age>0:
                alive += 1
                color = get_color(age)
                draw.rectangle(
                    (x*CELL_SIZE, y*CELL_SIZE,
                     (x+1)*CELL_SIZE, (y+1)*CELL_SIZE),
                    fill=color
                )
    return alive

def draw_bigbang(draw):
    cx = WIDTH_PX//2
    cy = HEIGHT_PX//2

    for _ in range(50):
        angle = random.random()*6.28
        length = random.randint(20,80)

        x = cx + math.cos(angle)*length
        y = cy + math.sin(angle)*length

        color = random.choice([
            (255,255,255),(255,255,0),(255,128,0),
            (255,0,0),(0,255,255),(0,255,0)
        ])

        draw.line((cx,cy,x,y), fill=color)

# ===== メイン =====
randomize()

try:
    while True:
        draw_obj = ImageDraw.Draw(image)

        if bigbang:
            draw_bigbang(draw_obj)
            draw_image()

            if time.time() - bigbang_time > 1:
                randomize()
            continue

        new = [[0]*WIDTH for _ in range(HEIGHT)]
        elapsed = time.time() - start_time
        birth = get_birth_prob(elapsed)

        for y in range(HEIGHT):
            for x in range(WIDTH):
                n = count_neighbors(x,y)

                if grid[y][x]:
                    if n in (2,3):
                        new[y][x] = grid[y][x] + 1
                else:
                    if n==3 and random.random()<birth:
                        new[y][x] = 1

        grid[:] = new

        if elapsed>60 and not boost1_done:
            add_cells(); boost1_done=True

        if elapsed>90 and not boost2_done:
            add_cells(); boost2_done=True

        if elapsed>105:
            grid[:] = move_center()
            if is_centered():
                bigbang=True
                bigbang_time=time.time()

        alive = draw(draw_obj)

        if alive==0 or elapsed>RESTART_TIME:
            randomize()

        draw_image()
        time.sleep(0.08)

except KeyboardInterrupt:
    pass

finally:
    pi.write(BACKLIGHT_PIN, 0)  # ★終了時OFF
    pi.spi_close(spi)
    pi.stop()