"""Hardware bring-up tool for TP-002 (LSN-A-0001). A test tool, not the product software.

Reads the BME280 (0x77) and SGP40 (0x59) once a second and prints one CSV line per reading:
local time, temperature (C), humidity (%RH), pressure (hPa), VOC index. The SGP40 VOC index
needs readings every second and settles after about an hour (Sensirion SGP40 datasheet v1.2).

Run on the unit (Raspberry Pi OS with I2C enabled):
    pip install adafruit-blinka adafruit-circuitpython-bme280 adafruit-circuitpython-sgp40
    python3 bringup.py | tee bringup_<serial>.csv
Stop with Ctrl+C.
"""
import time
from datetime import datetime

import board
import adafruit_sgp40
from adafruit_bme280 import basic as adafruit_bme280


def main():
    i2c = board.I2C()
    bme = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x77)  # SparkFun board default
    sgp = adafruit_sgp40.SGP40(i2c)                                 # fixed address 0x59
    print("time,temperature_c,humidity_pct,pressure_hpa,voc_index")
    while True:
        t, rh, p = bme.temperature, bme.humidity, bme.pressure
        voc = sgp.measure_index(temperature=t, relative_humidity=rh)
        print(f"{datetime.now().isoformat(timespec='seconds')},{t:.2f},{rh:.2f},{p:.2f},{voc}", flush=True)
        time.sleep(1)


if __name__ == "__main__":
    main()
