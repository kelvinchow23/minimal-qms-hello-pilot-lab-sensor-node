#!/usr/bin/env python3
"""Test receiver (test equipment EQ-001, not part of the product).

Accepts POST /reading and appends each reading, with its receive time, to readings.jsonl.
Run it on an NTP-synced computer on the lab network or Tailscale:  python receiver.py 8080
"""
import json
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        rec = json.loads(body)
        rec["received"] = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
        with open("readings.jsonl", "a") as f:
            f.write(json.dumps(rec) + "\n")
        self.send_response(204)
        self.end_headers()

    def log_message(self, *args):
        pass


port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
HTTPServer(("", port), Handler).serve_forever()
