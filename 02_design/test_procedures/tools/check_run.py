#!/usr/bin/env python3
"""Summarize readings.jsonl for TP-001, TP-003 and TP-004.

For each unit: number of readings, largest gap between received readings, largest
|unit time - receive time|, missing fields, and the maximum CPU temperature.
Usage: python check_run.py readings.jsonl [unit]
"""
import json
import sys
from datetime import datetime

FIELDS = ["temperature_c", "humidity_pct", "pressure_hpa", "voc_index"]

rows = [json.loads(line) for line in open(sys.argv[1]) if line.strip()]
units = [sys.argv[2]] if len(sys.argv) > 2 else sorted({r["unit"] for r in rows})
for u in units:
    rs = [r for r in rows if r["unit"] == u]
    rec = [datetime.fromisoformat(r["received"]) for r in rs]
    gaps = [(b - a).total_seconds() for a, b in zip(rec, rec[1:])]
    offsets = [abs((datetime.fromisoformat(r["t"]) - datetime.fromisoformat(r["received"])).total_seconds())
               for r in rs]
    missing = sorted({f for r in rs for f in FIELDS if r.get(f) is None})
    unsynced = sum(1 for r in rs if not r.get("time_synced"))
    cpu = [r["cpu_temp_c"] for r in rs if r.get("cpu_temp_c") is not None]
    print(f"{u}: {len(rs)} readings, {rec[0]} to {rec[-1]}")
    print(f"  largest gap {max(gaps, default=0):.1f} s (limit 10 s); gaps over 10 s: {sum(g > 10 for g in gaps)}")
    print(f"  largest time offset {max(offsets, default=0):.2f} s (limit 1 s); unsynced readings: {unsynced}")
    print(f"  missing fields: {missing or 'none'}; max CPU temperature: {max(cpu) if cpu else 'n/a'} C")
