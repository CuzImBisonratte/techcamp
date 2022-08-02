from network_esp32 import wifi

wifi.reset()

enc_str = ["OPEN", "", "WPA PSK", "WPA2 PSK", "WPA/WPA2 PSK", "", "", ""]
aps = wifi.nic.scan()

for ap in aps:
    print(aps)
