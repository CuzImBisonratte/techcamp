
import sensor, image, lcd, time

lcd.init()

clock = time.clock()

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)

sensor.run(1)

sensor.skip_frames(20)

while 1:
    clock.tick()
    img = sensor.snapshot()
    fps = clock.fps()
    img.draw_string(2, 2, ("%2.1ffps" %(fps)), color=(255,0,0), scale=3)
    lcd.display(img)
