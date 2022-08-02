import image
import lcd
import time

lcd.init(freq=15000000)

img = image.Image("/sd/iamgeessss/regio.jpg")


tim = time.time()
while 1:
    lcd.display(img)
    if time.time() -tim >2:
        break

tim = time.time()
while 1:
    lcd.mirror(1)
    lcd.display(img)
    if time.time() -tim >2:
        break

lcd.mirror(0)
tim = time.time()
while 1:
    lcd.display(img,(50,50,50,50))
    if time.time() -tim >2:
        break

lcd.clear()
