import image, lcd, time, audio
from Maix import GPIO, I2S
from fpioa_manager import fm

# user settings
sample_rate   = 16000
record_time   = 4  #s

# default settings
sample_points = 2048
wav_ch        = 2

fm.register(8,  fm.fpioa.GPIO0, force=True)
wifi_en = GPIO(GPIO.GPIO0, GPIO.OUT)
wifi_en.value(0)

fm.register(20,fm.fpioa.I2S0_IN_D0, force=True)
fm.register(19,fm.fpioa.I2S0_WS, force=True)
fm.register(18,fm.fpioa.I2S0_SCLK, force=True)

rx = I2S(I2S.DEVICE_0)
rx.channel_config(rx.CHANNEL_0, rx.RECEIVER, align_mode=I2S.STANDARD_MODE)
rx.set_sample_rate(sample_rate)
print(rx)

recorder = audio.Audio(path="/sd/record.wav", is_create=True, samplerate=sample_rate)

queue = []

frame_cnt = record_time*sample_rate//sample_points

for i in range(frame_cnt):
    tmp = rx.record(sample_points*wav_ch)
    if len(queue) > 0:
        ret = recorder.record(queue[0])
        queue.pop(0)
    rx.wait_record()
    queue.append(tmp)
    print(str(i) + ":" + str(time.ticks()))

recorder.finish()
