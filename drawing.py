import lcd, image
from fpioa_manager import fm
from Maix import GPIO
from board import board_info

lcd.init()

img = image.Image()
img.draw_string(120,120, "Hello")
lcd.display(img)

fm.register(board_info.BOOT_KEY, fm.fpioa.GPIOHS0)
key = GPIO(GPIO.GPIOHS0, GPIO.PULL_UP)

while 1:
    if key.value() == 0:
        img.clear()
        img.draw_string(120,120, "Goodbye")
        lcd.display(img)
        break
