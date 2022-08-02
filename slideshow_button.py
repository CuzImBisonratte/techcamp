files = ("cat", "cat_small", "cat2", "cat3", "regio", "tambako", "train", "traindock")
import image, lcd, time, random
from Maix import GPIO
from fpioa_manager import fm

lcd.init()

tim = time.time()
while 1:
    fm.register(16,fm.fpioa.GPIO0)
    button = GPIO(GPIO.GPIO0, GPIO.IN)
    if button.value == "1":
        randomfile = "/sd/images/" + files[random.randint(0,len(files)-1)] + ".jpg"
        img = image.Image(randomfile)
        lcd.display(img)
    time.sleep(1)
