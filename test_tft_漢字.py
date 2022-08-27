"""
ＴＦＴ液晶の性能評価

文字の大きさと色を変えて漢字を表示
本日は晴天なり本日は晴天な
本日は晴天なり本日は晴天な
本日は晴天なり本日は晴天な

lcd177.py の　DISP_rotationを0,90,180,270で変更すると表示向きを変えられる


"""
import lcd177
import time

def main():

    lcd177.init('on')

    print('abcdefghijklmnopqrstuvqxyz')
    mes= '本日は晴天なり本日は晴天な'
    lcd177.disp(mes,12,'white')

    print('12345678901234567890')
    mes= '本日は晴天なり本日は'
    lcd177.disp(mes,16,'blue')

    print('1234567890123456')
    mes= '本日は晴天なり本り'
    lcd177.disp(mes,20,'red')

    print('1234567890123')
    mes= '本日は晴天な'
    lcd177.disp(mes,24,'green')

    print('12345678901')
    mes= '本日は晴天'
    lcd177.disp(mes,28,'white')

    time.sleep(2)


if __name__ == "__main__":
    main()
