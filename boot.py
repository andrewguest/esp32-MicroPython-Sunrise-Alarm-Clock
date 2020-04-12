import network
import esp
import gc
import os
from time import sleep
from dotenv import load_dotenv


load_dotenv()
gc.enable()
esp.osdebug(None)

sleep(2)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ssid = os.getenv("wifi_ssid")
password = os.getenv("wifi_password")
wlan.connect(ssid, password)

while wlan.isconnected() == False:
    print("Connecting to WiFi...")
    sleep(1)

if wlan.isconnected():
    print("[+] Connected!")
