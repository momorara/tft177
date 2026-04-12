import pigpio
from gpiozero import Button, PWMLED, DigitalOutputDevice
from PIL import Image, ImageDraw
import time
import random

# ===== ピン =====
DC_PIN = 25
RESET_PIN = 24
BACKLIGHT_PIN = 12

SPI_DEVICE = 0
SPI_SPEED_HZ = 4000000

# ===== 入力 =====
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
WIDTH = 160
HEIGHT = 128
image = Image.new("RGB", (WIDTH, HEIGHT), "black")

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
    send_command(0x2A); send_data([0,0,0,WIDTH-1])
    send_command(0x2B); send_data([0,0,0,HEIGHT-1])
    send_command(0x2C)

    px = dsp.load()
    data = []
    for y in range(HEIGHT):
        for x in range(WIDTH):
            r,g,b = px[x,y]
            c = ((r & 0xF8)<<8)|((g & 0xFC)<<3)|(b>>3)
            data.append((c>>8)&0xFF)
            data.append(c&0xFF)
    send_data(data)

init_display()

# ===== テトリス設定 =====
GRID_W = 10
GRID_H = 16
BLOCK = 8

offset_x = (WIDTH - GRID_W * BLOCK) // 2

COLORS = [
    "red", "yellow", "green", "white",
    "blue", "cyan", "magenta",
    "orange", "purple", "pink",
    "lime", "gold", "skyblue"
]

last_color = None

def get_random_color():
    global last_color
    color = random.choice(COLORS)
    while color == last_color:
        color = random.choice(COLORS)
    last_color = color
    return color

grid = [[None for _ in range(GRID_W)] for _ in range(GRID_H)]

SHAPES = [
    [(0,0),(1,0),(0,1),(1,1)],
    [(0,0),(1,0),(2,0),(3,0)],
    [(0,0),(1,0),(2,0),(1,1)],
    [(0,0),(0,1),(1,1),(2,1)],
]

def new_piece():
    return {
        "shape": random.choice(SHAPES),
        "x": 4,
        "y": 0,
        "color": get_random_color()
    }

piece = new_piece()
score = 0
game_over = False

# ===== 回転 =====
def rotate(shape):
    return [(y, -x) for x, y in shape]

def try_rotate():
    global piece
    new_shape = rotate(piece["shape"])
    min_x = min(x for x, y in new_shape)
    min_y = min(y for x, y in new_shape)
    adjusted = [(x - min_x, y - min_y) for x, y in new_shape]

    if not collision(piece["x"], piece["y"], adjusted):
        piece["shape"] = adjusted

# ===== 判定 =====
def collision(px, py, shape):
    for x,y in shape:
        gx = px + x
        gy = py + y
        if gx < 0 or gx >= GRID_W or gy >= GRID_H:
            return True
        if gy >= 0 and grid[gy][gx]:
            return True
    return False

# ===== 固定 =====
def lock_piece():
    global piece
    for x,y in piece["shape"]:
        gx = piece["x"] + x
        gy = piece["y"] + y
        if gy >= 0:
            grid[gy][gx] = piece["color"]
    piece = new_piece()

# ===== ライン消去 =====
def clear_lines():
    global score
    new_grid = []
    cleared = 0

    for row in grid:
        if all(row):
            cleared += 1
        else:
            new_grid.append(row)

    while len(new_grid) < GRID_H:
        new_grid.insert(0, [None]*GRID_W)

    score += cleared
    return new_grid

# ===== 描画 =====
def draw():
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,WIDTH,HEIGHT), fill="black")

    draw.line((offset_x-2,0, offset_x-2, GRID_H*BLOCK), fill="white", width=2)
    draw.line((offset_x+GRID_W*BLOCK+2,0,
               offset_x+GRID_W*BLOCK+2, GRID_H*BLOCK), fill="white", width=2)

    for y in range(GRID_H):
        for x in range(GRID_W):
            if grid[y][x]:
                draw.rectangle((
                    offset_x + x*BLOCK,
                    y*BLOCK,
                    offset_x + (x+1)*BLOCK,
                    (y+1)*BLOCK),
                    fill=grid[y][x])

    for x,y in piece["shape"]:
        draw.rectangle((
            offset_x + (piece["x"]+x)*BLOCK,
            (piece["y"]+y)*BLOCK,
            offset_x + (piece["x"]+x+1)*BLOCK,
            (piece["y"]+y+1)*BLOCK),
            fill=piece["color"])

    draw.text((5,5), f"{score}", fill="white")
    draw_image()

# ===== メイン =====
try:
    drop_timer = 0
    rotate_pressed = False

    while not game_over:

        # 回転
        if SW_1.is_pressed and SW_2.is_pressed:
            if not rotate_pressed:
                try_rotate()
                rotate_pressed = True
        else:
            rotate_pressed = False

            if SW_1.is_pressed:
                if not collision(piece["x"]+1, piece["y"], piece["shape"]):
                    piece["x"] += 1

            elif SW_2.is_pressed:
                if not collision(piece["x"]-1, piece["y"], piece["shape"]):
                    piece["x"] -= 1

        # ★ スピード制御（ここが追加）
        speed = max(3, 10 - (score // 2))

        drop_timer += 1
        if drop_timer > speed:
            drop_timer = 0

            if not collision(piece["x"], piece["y"]+1, piece["shape"]):
                piece["y"] += 1
            else:
                lock_piece()
                grid = clear_lines()

                if collision(piece["x"], piece["y"], piece["shape"]):
                    game_over = True

        draw()
        time.sleep(0.05)

    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,WIDTH,HEIGHT), fill="black")
    draw.text((40,50), "GAME OVER", fill="white")
    draw.text((40,70), f"{score}", fill="white")
    draw_image()
    time.sleep(5)

except KeyboardInterrupt:
    pass

finally:
    pi.spi_close(spi)
    pi.stop()