# LSN node software v0.1.0

Runs on the Raspberry Pi Zero 2 W (ECM-0004) of LSN-A-0001. Reads the BME280 and SGP40 and
sends a JSON reading to a server every 10 s.

**Monitoring only. The lab sensor node is not a certified safety or gas alarm.** (REQ-015)

## Install (per unit, during the build)
1. Flash Raspberry Pi OS Lite (64-bit) to the SD card (ECX-0001) with Raspberry Pi Imager.
   Set the hostname to the unit's serial number. Enter Wi-Fi details in Imager or on the unit,
   never in this repo (REQ-010).
2. Boot, then enable I2C: `sudo raspi-config nonint do_i2c 0`.
3. Join the lab network (enterprise login) and Tailscale, following lab IT's instructions.
4. Install:
   ```
   sudo mkdir -p /opt/lsn-node && sudo cp lsn_node.py /opt/lsn-node/
   sudo python3 -m venv /opt/lsn-node/venv
   sudo /opt/lsn-node/venv/bin/pip install -r requirements.txt
   ```
5. Create `/etc/lsn-node.conf`:
   ```
   [node]
   server_url = http://<server>:8080/reading
   interval_s = 10
   ```
6. `sudo cp lsn-node.service /etc/systemd/system/ && sudo systemctl enable --now lsn-node`
7. Check: `journalctl -u lsn-node -f` shows no errors, and the server receives readings.
8. Protect the SD card against power cuts (RISK-003): `sudo raspi-config nonint enable_overlayfs`,
   then reboot. Disable the overlay first to change the configuration later.

## Reading format
JSON object: `unit`, `software`, `seq`, `t` (UTC, ISO 8601), `time_synced`, `temperature_c`,
`humidity_pct`, `pressure_hpa`, `voc_index`, `cpu_temp_c`.

## Notes
- Library versions are not pinned yet. Record the installed versions (`pip freeze`) in the
  build record of the first unit, and pin them at G4.
- Not yet run on hardware.
