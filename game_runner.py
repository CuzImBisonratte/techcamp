import nes, lcd
from fpioa_manager import fm
from board import board_info
from Maix import I2S,GPIO

# need to run config_maix_duino.py first to create the config file needed
# (prob can do this programmatically if needed with an import?)

WIFI_EN_PIN = 8
# disable wifi - doesn't seem to be needed but I guess it saves some electricity!
fm.register(WIFI_EN_PIN, fm.fpioa.GPIO0, force=True)
wifi_en = GPIO(GPIO.GPIO0, GPIO.OUT)
wifi_en.value(0)

# register i2s(i2s0) pin
fm.register(34, fm.fpioa.I2S0_OUT_D1, force=True)
fm.register(35, fm.fpioa.I2S0_SCLK, force=True)
fm.register(33, fm.fpioa.I2S0_WS, force=True)

# init i2s(i2s0)
wav_dev = I2S(I2S.DEVICE_0)
wav_dev.channel_config(wav_dev.CHANNEL_1, I2S.TRANSMITTER, resolution=I2S.RESOLUTION_16_BIT,
                       cycles=I2S.SCLK_CYCLES_32, align_mode=I2S.RIGHT_JUSTIFYING_MODE)

fm.register(board_info.PIN2, fm.fpioa.GPIOHS21)
fm.register(board_info.PIN3, fm.fpioa.GPIOHS22)
fm.register(board_info.PIN4, fm.fpioa.GPIOHS23)
fm.register(board_info.PIN5, fm.fpioa.GPIOHS24)

lcd.init(freq=15000000)
nes.init(nes.JOYSTICK, cs=fm.fpioa.GPIOHS21, clk=fm.fpioa.GPIOHS22, mosi=fm.fpioa.GPIOHS23, miso=fm.fpioa.GPIOHS24)

# this loads nova the squirrel - google this OS game
# N.B. R1/R2 control volume!
nes.load("/sd/Super_mario_brothers.nes")

while True:
    nes.loop()
