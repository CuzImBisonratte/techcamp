import lcd, time
from fpioa_manager import fm
from Maix import GPIO, I2S
import video

lcd.init()
AUDIO_PA_EN_PIN = 2
i2s = I2S(I2S.DEVICE_0)

i2s.channel_config(i2s.CHANNEL_1, I2S.TRANSMITTER, resolution=I2S.RESOLUTION_16_BIT,cycles=I2S.SCLK_CYCLES_32, align_mode=I2S.RIGHT_JUSTIFYING_MODE)

if AUDIO_PA_EN_PIN:
    fm.register(AUDIO_PA_EN_PIN, fm.fpioa.GPIO1, force=True)
    wifi_en = GPIO(GPIO.GPIO1, GPIO.OUT)
    wifi_en.value(1)

fm.register(34,  fm.fpioa.I2S0_OUT_D1, force=True)
fm.register(35,  fm.fpioa.I2S0_SCLK, force=True)
fm.register(33,  fm.fpioa.I2S0_WS, force=True)

v = video.open("/sd/bad.avi")
print(v)
v.volume(05)
while True:
    if v.play() == 0:
        print("play end")
        break
v.__del__()
