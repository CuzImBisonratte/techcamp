# Import all needed libraries
import sensor, image, lcd, time, sys, gc
import KPU as kpu

# Define the main function
def main(labels = None,model_addr=0x300000,lcd_rotation=0,sensor_hmirror=False,sensor_vflip=False):

    # Run the garbage collector
    gc.collect()
    # Reset the sensor
    sensor.reset()
    # Set up the sensor
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_windowing((224, 224))
    # Start the sensor
    sensor.run(1)

    # Initialize the lcd
    lcd.init(type=1)
    # Reset the rotation
    lcd.rotation(lcd_rotation)
    # Clear the lcd to be white
    lcd.clear(lcd.WHITE)

    # Check if labels are not found
    if not labels:
        # Raise an exception
        raise Exception("no labels.txt")

    # Register a new kpu task
    task = kpu.load(model_addr)

    # Try looping
    try:
        while 1:
            # Take a shot
            img = sensor.snapshot()
            # Add 1 to t time
            t = time.ticks_ms()
            # Set up processor finding
            fmap = kpu.forward(task, img)
            # Add 1 to t time
            t = time.ticks_ms()
            # Create a list to track object positions
            plist = fmap[:]
            # Set end of list
            pmax=max(plist)
            # Get the highest index
            max_index=plist.index(pmax)

            # Check if pmax is under 1.5
            if (pmax < 1.5):
                img.draw_string(0,0, "Cannot label object", scale=2, color=(255, 0, 0))
            else:
                # Add a label to the object
                img.draw_string(0,0, "%.2f %s" %(pmax, labels[max_index].strip()), scale=2, color=(255, 255, 255))
            lcd.display(img)

    # Check exception
    except Exception as e:
        # Print out exception
        sys.print_exception(e)
    # Run final
    finally:
        # Deinitiate the kpu task
        kpu.deinit(task)


# Define main invocation
if __name__ == "__main__":
    # Start a new try exception
    try:
        # Open the file
        with open("labels.txt") as f:

            # Init a variable containing the list of labels
            labels = f.readlines()

        # Invoke main function
        main(labels=labels, model_addr=0x300000, lcd_rotation=0, sensor_hmirror=False, sensor_vflip=False)

    # Exception
    except Exception as e:
        # Print out error
        sys.print_exception(e)
    # Finally
    finally:
        # Collect memory
        gc.collect()
