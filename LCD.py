from time import sleep
from time import gmtime, strftime
import datetime
import smbus

# Define some device parameters
I2C_ADDR = 0x27  # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1      # Mode - Sending data
LCD_CMD = 0      # Mode - Sending command

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line

# Define backlight control
LCD_BACKLIGHT_ON = 0x08
LCD_BACKLIGHT_OFF = 0x00

ENABLE = 0b00000100  # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# Open I2C interface
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def lcd_init():
    # Initialise display
    lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
    lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
    lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
    sleep(E_DELAY)

def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = the data
    # mode = 1 for data
    #        0 for command

    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT_ON
    bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT_ON

    # High bits
    bus.write_byte(I2C_ADDR, bits_high)
    lcd_toggle_enable(bits_high)

    # Low bits
    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
    # Toggle enable
    sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    sleep(E_PULSE)
    bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
    sleep(E_DELAY)

def lcd_string(message, line):
    # Send string to display
    message = message.ljust(LCD_WIDTH, " ")
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

def main():
    # Main program block
    # Initialise display
    lcd_init()
    while True:
        local_time = datetime.datetime.now()
        lcd_string(strftime("%Y.%m.%d (%a)", gmtime()), LCD_LINE_1)
        lcd_string(local_time.strftime("%H:%M"), LCD_LINE_2)
        sleep(1)

        local_time = datetime.datetime.now()
        lcd_string(strftime("%Y.%m.%d (%a)", gmtime()), LCD_LINE_1)
        lcd_string(local_time.strftime("%H %M"), LCD_LINE_2)
        sleep(1)

try:
    print('Start:' + str(datetime.datetime.now()))
    main()
except KeyboardInterrupt:
    pass
finally:
    LCD_BACKLIGHT = LCD_BACKLIGHT_OFF  # バックライトオフ
    lcd_byte(0x01, LCD_CMD)  # 表示内容クリア
    # GPIO.cleanup()  # GPIOピンの初期化
