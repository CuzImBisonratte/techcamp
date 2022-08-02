files = ("cat", "cat_small", "cat2", "cat3", "regio", "tambako", "train", "traindock")
import image, lcd, time, random

lcd.init()


tim = time.time()
while 1:
    randomfile = "/sd/images/" + files[random.randint(0,len(files)-1)] + ".jpg"
    print(randomfile)
    img = image.Image(randomfile)
    lcd.display(img)
    time.sleep(3)
