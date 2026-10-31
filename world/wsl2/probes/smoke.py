"""Trusted bounded W0 probe, not a developing organism."""
import json
import os
import time

request = json.loads(input())
print(json.dumps({"type": "heartbeat", "seq": 0, "timestamp": time.time()}), flush=True)
print(json.dumps({"type": "result", "seed": request["seed"], "uid": os.getuid(),
                  "message": "trusted smoke probe"}), flush=True)
