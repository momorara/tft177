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

"""


import lcd177
import time
from PIL import Image, ImageDraw, ImageFont

def main():

    lcd177.init('on')

    dsp_file = "ねこ.jpg"
    lcd177.dsp_file(dsp_file)
    time.sleep(1)
    lcd177.init('reset')

    dsp_file = "女性.jpg"
    lcd177.dsp_file(dsp_file)
    time.sleep(1)
    # lcd177.init('reset')   

    dsp_file = "夕日.jpg"
    lcd177.dsp_file(dsp_file)
    time.sleep(1)
    # lcd177.init('reset')   

    dsp_file = "自転車と男性.jpg"
    lcd177.dsp_file(dsp_file)
    time.sleep(1)


    lcd177.init('reset')    
    time.sleep(2)
    lcd177.init('off')


if __name__ == "__main__":
    main()
