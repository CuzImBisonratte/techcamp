import time, network
from Maix import GPIO
from fpioa_manager import fm

class wifi():
    nic = None

    def reset(force=False, reply=5, is_hard=True):
        if force == False and __class__.isconnected():
            return True

        try:
            fm.register(25,fm.fpioa.GPIOHS10)
            fm.register(8,fm.fpioa.GPIOHS11)
            fm.register(9,fm.fpioa.GPIOHS12)

            if is_hard:
                print("Use Hardware SPI for other maixduino")
                fm.register(28,fm.fpioa.SPI1_D0, force=True)
                fm.register(26,fm.fpioa.SPI1_D1, force=True)
                fm.register(27,fm.fpioa.SPI1_SCLK, force=True)
                __class__.nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10, rst=fm.fpioa.GPIOHS11, rdy=fm.fpioa.GPIOHS12, spi=1)
                print("ESP32_SPI firmware version:", __class__.nic.version())
            else:
                print("Use Software SPI for other hardware")
                fm.register(28,fm.fpioa.GPIOHS13, force=True)
                fm.register(26,fm.fpioa.GPIOHS14, force=True)
                fm.register(27,fm.fpioa.GPIOHS15, force=True)
                __class__.nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10,rst=fm.fpioa.GPIOHS11,rdy=fm.fpioa.GPIOHS12, mosi=fm.fpioa.GPIOHS13,miso=fm.fpioa.GPIOHS14,sclk=fm.fpioa.GPIOHS15)
                print("ESP32_SPI firmware version:", __class__.nic.version())

        except Exception as e:
            print(e)
            return 0
        return 1

    def connect(ssid="wifi_name",pasw="password"):
        if __class__.nic != None:
            return __class__.nic.connect(ssid, pasw)

    def ifconfig():
        if __class__.nic != None:
            return __class__.nic.ifconfig()

    def isconnected():
        if __class__.nic != None:
            return __class__.nic.isconnected()
        return False

if __name__ == "__main__":
    # from network_esp32 import wifi
    SSID = ""
    PASW = ""

def check_wifi_net(reply=5):
    if wifi.isconnected() != True:
        for i in range(reply):
            try:
                wifi.reset(is_hard=True)
                print('try esp32spi connect wifi...')
                wifi.connect(SSID, PASW)
                if wifi.isconnected():
                    break
            except Exception as e:
                print(e)
    return wifi.isconnected()

if wifi.isconnected() == False:
        check_wifi_net()
        print('network state:', wifi.isconnected(), wifi.ifconfig())

import socket
sock = socket.socket()
# the code goes here
sock.close()
