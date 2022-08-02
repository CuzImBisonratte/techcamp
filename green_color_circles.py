
import sensor, image, lcd, time

lcd.init()


sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)

sensor.run(1)

green_threshold_values = (0, 80, -70, -10, -0, 30)

while 1:
    current_image = sensor.snapshot()
    current_image_green_blobs = current_image.find_blobs([green_threshold_values])

    if current_image_green_blobs:
        for i in current_image_green_blobs:
            # tmp_green_blob = current_image.draw_rectangle(i[0:4])
            # tmp_green_blob = current_image.draw_cross(i[5], i[6])
            tmp_green_blob = current_image.draw_circle(i[5], i[6], i[3])
            lcd.display(current_image)
