"""
ＴＦＴ液晶の性能評価

文字の大きさと色を変えて漢字を表示
本日は晴天なり本日は晴天な
本日は晴天なり本日は晴天な
本日は晴天なり本日は晴天な

lcd177_1.py の　DISP_rotationを0,90,180,270で変更すると表示向きを変えられる

2024/02/10  ターミナルプロックの位置に対応するプログラムの整理
"""
import lcd177_1
import time

def main():

    lcd177_1.init('on')

    print('本日は晴天なり本日は晴天な')
    mes= '本日は晴天なり本日は晴天な'
    lcd177_1.disp(mes,12,'white')

    print('本日は晴天なり本日は晴天な')
    mes= '本日は晴天なり本日は'
    lcd177_1.disp(mes,16,'blue')

    print('本日は晴天なり本日は晴天な')
    mes= '本日は晴天なり本り'
    lcd177_1.disp(mes,20,'red')

    print('本日は晴天なり本日は晴天な')
    mes= '本日は晴天な'
    lcd177_1.disp(mes,24,'green')

    print('本日は晴天なり本日は晴天な')
    mes= '本日は晴天'
    lcd177_1.disp(mes,28,'white')

    time.sleep(2)

    lcd177_1.init('reset')
    lcd177_1.init('off')

if __name__ == "__main__":
    main()
