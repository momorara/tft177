"""
ＴＦＴ液晶の性能評価

文字の大きさと色を変えてアルファベットを表示
abcdefghijklmnopqrstuvqxyz
abcdefghijklmnopqrst
abcdefghijklmnop

lcd177.py の　DISP_rotationを0,90,180,270で変更すると表示向きを変えられる


"""
import lcd177
import time

def main():

    lcd177.init('on')

    mes= 'abcdefghijklmnopqrstuvqxyz'
    print(mes)
    lcd177.disp(mes,12,'white')

    mes= 'abcdefghijklmnopqrst'
    lcd177.disp(mes,16,'blue')

    mes= 'abcdefghijklmnop'
    lcd177.disp(mes,20,'red')

    mes= 'abcdefghijklm'
    lcd177.disp(mes,24,'green')

    mes= 'abcdefghijk'
    lcd177.disp(mes,28,'white')

    time.sleep(2)


if __name__ == "__main__":
    main()
