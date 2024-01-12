from gpiozero import InputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# センサーのピン設定
PIN_SR501 = 4

# 取得間隔
INTERVAL_TIME = 1.0

def main():
    # ピンを入力に設定(プルダウン設定)
    factory = PiGPIOFactory()
    sr501 = InputDevice(PIN_SR501, pull_up=False, pin_factory=factory)

    try:
        while True:
            if sr501.is_active:
                print("Motion detected.")
            else:
                print("no movement.")
            sleep(INTERVAL_TIME)
    except KeyboardInterrupt:
        print("stop")

    return

if __name__ == "__main__":
    main()
