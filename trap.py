from fpioa_manager import *
from Maix import GPIO, I2S
import audio, time
from board import board_info

fm.register(board_info.BOOT_KEY, fm.fpioa.GPIOHS0)
key = GPIO(GPIO.GPIOHS0, GPIO.PULL_UP)

WIFI_EN_PIN = 8
AUDIO_PA_EN_PIN = 32

# disable wifi
fm.register(WIFI_EN_PIN, fm.fpioa.GPIO0, force=True)
wifi_en = GPIO(GPIO.GPIO0, GPIO.OUT)
wifi_en.value(0)

# open audio PA
if AUDIO_PA_EN_PIN:
    fm.register(AUDIO_PA_EN_PIN, fm.fpioa.GPIO1, force=True)
    wifi_en = GPIO(GPIO.GPIO1, GPIO.OUT)
    wifi_en.value(1)

# register i2s(i2s0) pin
fm.register(34, fm.fpioa.I2S0_OUT_D1, force=True)
fm.register(35, fm.fpioa.I2S0_SCLK, force=True)
fm.register(33, fm.fpioa.I2S0_WS, force=True)

# init i2s(i2s0)
wav_dev = I2S(I2S.DEVICE_0)

# init audio
player = audio.Audio(path="/sd/never.wav")
player.volume(50)

# read audio info
wav_info = player.play_process(wav_dev)
print("wav file head information: ", wav_info)

# config i2s according to audio info
wav_dev.channel_config(wav_dev.CHANNEL_1, I2S.TRANSMITTER, resolution=I2S.RESOLUTION_16_BIT,cycles=I2S.SCLK_CYCLES_32, align_mode=I2S.RIGHT_JUSTIFYING_MODE)
wav_dev.set_sample_rate(wav_info[1])

# loop to play audio
while key.value() == 1:
    print("Waiting for button press")
while key.value() == 0:
    ret = player.play()
    if ret == None:
        print("format error")
        break
    elif ret == 0:
        print("end")
        break
player.finish()
time.sleep(1)
player = ""
time.sleep(1)

#
#
#
#
#

# init audio
player = audio.Audio(path="/sd/pianomoment.wav")
player.volume(50)

# read audio info
wav_info = player.play_process(wav_dev)
print("wav file head information: ", wav_info)

# config i2s according to audio info
wav_dev.channel_config(wav_dev.CHANNEL_1, I2S.TRANSMITTER, resolution=I2S.RESOLUTION_16_BIT,cycles=I2S.SCLK_CYCLES_32, align_mode=I2S.RIGHT_JUSTIFYING_MODE)
wav_dev.set_sample_rate(wav_info[1])

# loop to play audio
while key.value() == 1:
    print("Waiting for button press")
while key.value() == 0:
    ret = player.play()
    if ret == None:
        print("format error")
        break
    elif ret == 0:
        print("end")
        break
player.finish()
