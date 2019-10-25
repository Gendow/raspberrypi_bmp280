#!/usr/bin/env python3
import board
import busio
import adafruit_bmp280
import time
import datetime
import requests
import json
import threading
from config import apikey
 
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

def getSeaLevelPressure():
    threading.Timer(240, getSeaLevelPressure).start()
    req = requests.get('http://weerlive.nl/api/json-data-10min.php?key=%s&locatie=Arnhem' % apikey)

    if req.status_code == 200:
        payload = json.loads(req.text)
        sensor.sea_level_pressure = float(payload["liveweer"][0]["luchtd"])
        print("\n=======================")
        print("KNMI Sea Level Pressure: % 0.1f" % float(payload["liveweer"][0]["luchtd"]))
        print("=======================")
    else:
        print("error from weather API: %" % req.status-code)
  
getSeaLevelPressure()


while True:
    print("\nTemperature: %0.1f C" % sensor.temperature)
    print("Pressure: %0.1f hPa" % sensor.pressure)
    print("Altitude: %0.2f meters" % sensor.altitude)
    print("Sea Level Pressure: %0.1f hPa " % sensor.sea_level_pressure)
    print(datetime.datetime.now())
    time.sleep(10)
