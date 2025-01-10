"""
ＴＦＴ液晶の性能評価

文字の大きさと色を変えて数字を表示
12345678901234567890123456
12345678901234567890123
1234567890123456789

lcd177_1.py の　DISP_rotationを0,90,180,270で変更すると表示向きを変えられる

2024/02/10  ターミナルプロックの位置に対応するプログラムの整理
"""
import lcd177_1
import time

def main():

    lcd177_1.init('on')

    mes= '12345678901234567890123456'
    print(mes)
    lcd177_1.disp(mes,12,'white')

    mes= '12345678901234567890'
    lcd177_1.disp(mes,16,'blue')

    mes= '1234567890123456'
    lcd177_1.disp(mes,20,'red')

    mes= '1234567890123'
    lcd177_1.disp(mes,24,'green')

    mes= '12345678901'
    lcd177_1.disp(mes,28,'white')

    mes= '12345678901'
    lcd177_1.disp(mes,32,'blue')

    time.sleep(2)
    lcd177_1.init('off')
    lcd177_1.init('reset')

if __name__ == "__main__":
    main()
