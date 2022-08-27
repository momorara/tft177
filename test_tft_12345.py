"""
ＴＦＴ液晶の性能評価

文字の大きさと色を変えて数字を表示
12345678901234567890123456
12345678901234567890123
1234567890123456789

lcd177.py の　DISP_rotationを0,90,180,270で変更すると表示向きを変えられる


"""
import lcd177
import time

def main():

    lcd177.init('on')

    mes= '12345678901234567890123456'
    print(mes)
    lcd177.disp(mes,12,'white')

    mes= '12345678901234567890'
    lcd177.disp(mes,16,'blue')

    mes= '1234567890123456'
    lcd177.disp(mes,20,'red')

    mes= '1234567890123'
    lcd177.disp(mes,24,'green')

    mes= '12345678901'
    lcd177.disp(mes,28,'white')

    mes= '12345678901'
    lcd177.disp(mes,32,'blue')

    time.sleep(2)


if __name__ == "__main__":
    main()
