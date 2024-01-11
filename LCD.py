import smbus
import time
import datetime

# I2C通信設定
I2C_ADR = 0x27 # I2Cアドレス
LCD_WDT = 16 # 文字数上限
LCD_BKL = 0x08 # バックライトON
LIST = [0x33, 0x32, 0x06, 0x0C, 0x28, 0x01]

bus = smbus.SMBus(1) # 接続バスの番号指定

def initialize():
     for i in LIST:
          send_data(i, 0)
          time.sleep(0.0005)

def send_data(bits, mode):
     upbits = mode | (bits & 0xF0) | LCD_BKL
     lwbits = mode | ((bits<<4) & 0xF0) | LCD_BKL
     bus.write_byte(I2C_ADR, upbits)
     bus.write_byte(I2C_ADR, (upbits | 0b00000100))
     bus.write_byte(I2C_ADR, (upbits & ~0b00000100))
     bus.write_byte(I2C_ADR, lwbits)
     bus.write_byte(I2C_ADR, (lwbits | 0b00000100))
     bus.write_byte(I2C_ADR, (lwbits & ~0b00000100))

def set_display(message,line):
     message = message.center(LCD_WDT," ") # メッセージ表示　中央揃え
     send_data(line, 0)
     for i in range(LCD_WDT):
          send_data(ord(message[i]), 1)

# メイン処理
def main():
     initialize() # 初期化
     while True:
          # 現在時刻取得
          current_time = datetime.datetime.now() # 現在時刻取得
          set_display(time.strftime("%Y/%m/%d (%a)", time.gmtime()) , 0x80) # 1行目:年月日(曜日)表示
          set_display(current_time.strftime("%H:%M:%S"), 0xC0) # 2行目:現在時間表示
          time.sleep(0.1)

try:
     #mainを実行
     main()
except KeyboardInterrupt:
     # 例外処理(Ctrl+C)
     pass
finally:
     # 終了時に行う処理
     LCD_BKL = 0x00 # バックライトOFF
     send_data(0x01, 0) # LCD表示クリア
