#! /usr/bin/python
"""

openCVでpiCameraの画像を取り込み
液晶に表示する。

ライブラリのインストール
pip3 install adafruit-circuitpython-rgb-display

2022/06/14  start
    01      swでスタート、ストップを制御するのもいいね
2022/06/17  lcd177.pyを使う
            とりあえず、フレーム渡しで表示


"""
import RPi.GPIO as GPIO
import lcd177
import time
from PIL import Image, ImageDraw, ImageFont



# スタートスイッチとストップスイッチの設定
sw_start = 6
sw_stop  = 5
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(sw_start,GPIO.IN)
GPIO.setup(sw_stop,GPIO.IN)
def Read_sw_start():
    if GPIO.input(sw_start):return 'on'
    return 'off'

def Read_sw_stop():
    if GPIO.input(sw_stop):return 'on'
    return 'off'



# カメラからフレームを取り込み、液晶に表示する。
def getCameraFrames(fps):

    frame_deley_time   = (1/fps)*0.9
    # print(frame_deley_time_n)
    # print(total_frames, past_frames)
    
    # トリミングするにはopencvでデータを取り込む必要がありました。
    # cap = cv2.VideoCapture(0)


    # fps = FPS().start() # start the FPS counter
    while True:
        # カメラから1フレーム取り込みリストに追加
        # ret, frame = cap.read()

        frame = Image.open('ねこ.jpg')
        lcd177.dsp_frame(frame)

        # 録画中の画像確認　運用ではいらないかな
        # cv2.imshow("Recording", frames[len(frames)-1])
        # cv2.waitKey(1)


        # fpsに合ったディレイを作る
        start = time.time()
        parst = time.time()
        while parst-start < frame_deley_time:
            time.sleep(0.01)
            # ストップトリガー
            if Read_sw_stop() == 'on' :
                break 
        if Read_sw_stop() == 'on' :
            print('stop on')
            break 


    # stop the timer and display FPS information
    # fps.stop()
    # vs.stop()

    # cap.release()

    # print("[INFO] elasped time:  {:.2f}".format(fps.elapsed()))
    # print("[INFO] approx. FPS :   {:.2f}".format(fps.fps()))
    # print("[INFO] frame n     :  {:.2f}".format(len(frames)))

    time.sleep(2)
    cv2.destroyAllWindows()
    return 



def main():

    print('start')
    while True:
        time.sleep(0.01)
        # スタートトリガー
        if Read_sw_start() == 'on' :
            print('start on')
            break 
    # fps = 4
    lcd177.init('on')

    frame = Image.open('ねこ.jpg')
    lcd177.dsp_frame(frame)
    time.sleep(1)

    frame = Image.open('夕日.jpg')
    lcd177.dsp_frame(frame)
    time.sleep(1)

    frame = Image.open('女性.jpg')
    lcd177.dsp_frame(frame)
    time.sleep(1)

    # getCameraFrames(fps)
    print('stop')
    while True:
        time.sleep(0.01)
        # ストップトリガー
        if Read_sw_stop() == 'on' :
            print('stop on')
            break 
    lcd177.init('off')
    time.sleep(1)
    lcd177.init('reset')


if __name__ == '__main__':
    try:
        main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        print('key in stop')
    except ValueError as e:
        print(e)
