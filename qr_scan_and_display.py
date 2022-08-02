import sensor, image, lcd, time

lcd.init()

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)

# sensor.skip_frames(20)

sharp = (-1,-1,-1,-1,9,-1,-1,-1,-1)
edge = (-1,-1,-1,-1,8,-1,-1,-1,-1)
relievo = (2,0,0,0,-1,0,0,0,-1)
origin = (0,0,0, 0,1,0, 0,0,0)

tim = time.time()
while 1:
    img = sensor.snapshot()
    img.conv3(edge)
    lcd.display(img)
    if time.time() - tim > 10:
        break

tim = time.time()
while 1:
    img = sensor.snapshot()
    img.conv3(sharp)
    if time.time() - tim > 10:
        break

tim = time.time()
while 1:
    img = sensor.snapshot()
    img.conv3(relievo)
    if time.time() - tim > 10:
        break

lcd.clear()
