# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Released under the MIT license
https://github.com/YukinobuKurata/YouTubeMagicBuyButton/blob/master/MIT-LICENSE.txt

Be sure to check the learn guides for more usage information.

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!

Author(s): Melissa LeBlanc-Williams for Adafruit Industries

https://learn.adafruit.com/1-8-tft-display/python-usage
のページに手を加えた

画像の大きさが液晶と一致しなくても調整して取り敢えず表示します。

2022/04/09  使いやすいように改変した
2022/06/13  読み込む画像データがRGBで、液晶はGBRなので色変換が必要
2022/06/17  ファイル名で表示
2024/02/10  ターミナルプロックの位置に対応するプログラムの整理
"""


import lcd177_1
import time
from PIL import Image, ImageDraw, ImageFont

def main():

    lcd177_1.init('on')

    for i in range(1,8):
        dsp_file = "/home/pi/tft177/photo/ph_" + str(i) + ".JPG"
        lcd177_1.dsp_file(dsp_file)
        time.sleep(2)

    time.sleep(2)
    lcd177_1.init('off')
    lcd177_1.init('reset')


if __name__ == "__main__":
    main()
