#!/usr/bin/env python3
"""LSN lab sensor node (LSN-A-0001) software v0.1.0.

Reads the SGP40 VOC index every second (its algorithm needs 1 Hz samples) and, every
interval_s seconds, reads the BME280 and sends one reading to the server as JSON over HTTP.
Readings that cannot be sent are dropped: recovering lost readings is out of scope.

Monitoring only. This is not a certified safety or gas alarm (REQ-015).
"""
import configparser
import json
import logging
import socket
import subprocess
import time
import urllib.request
from datetime import datetime, timezone

import board
import adafruit_sgp40
from adafruit_bme280 import basic as adafruit_bme280

VERSION = "0.1.0"
CONF_PATH = "/etc/lsn-node.conf"  # the server URL lives on the unit, never in the repo (REQ-010)


def load_config():
    cp = configparser.ConfigParser()
    cp.read(CONF_PATH)
    node = cp["node"] if "node" in cp else {}
    return node.get("server_url", ""), float(node.get("interval_s", "10"))


def time_synced():
    try:
        out = subprocess.run(["timedatectl", "show", "-p", "NTPSynchronized", "--value"],
                             capture_output=True, text=True, timeout=2).stdout.strip()
        return out == "yes"
    except Exception:
        return False


def cpu_temp_c():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return round(int(f.read()) / 1000, 1)
    except Exception:
        return None


def post(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=3) as r:
        return r.status


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    url, interval = load_config()
    if not url:
        logging.error("no server_url in %s", CONF_PATH)
    i2c = board.I2C()
    bme = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x77)  # SparkFun board default
    sgp = adafruit_sgp40.SGP40(i2c)
    unit = socket.gethostname()
    seq = 0
    next_report = time.monotonic()
    voc = None
    while True:
        t0 = time.monotonic()
        try:
            voc = sgp.measure_index(temperature=bme.temperature, relative_humidity=bme.humidity)
        except Exception as e:
            logging.warning("SGP40 read failed: %s", e)
        if t0 >= next_report:
            next_report += interval
            try:
                payload = {
                    "unit": unit,
                    "software": VERSION,
                    "seq": seq,
                    "t": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
                    "time_synced": time_synced(),
                    "temperature_c": round(bme.temperature, 2),
                    "humidity_pct": round(bme.humidity, 2),
                    "pressure_hpa": round(bme.pressure, 2),
                    "voc_index": voc,
                    "cpu_temp_c": cpu_temp_c(),
                }
                seq += 1
                if url:
                    post(url, payload)
            except Exception as e:
                logging.warning("reading not sent: %s", e)
        time.sleep(max(0.0, 1.0 - (time.monotonic() - t0)))


if __name__ == "__main__":
    main()
