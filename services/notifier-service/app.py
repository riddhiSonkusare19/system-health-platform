import os
import time
import threading
from collections import deque
from flask import Flask, jsonify
import requests

app = Flask(__name__)
HEALTH_URL = os.environ.get("HEALTH_SERVICE_URL", "http://localhost:5000")
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL_SECONDS", "10"))

alerts = deque(maxlen=50)


def poll_health():
    while True:
        try:
            r = requests.get(f"{HEALTH_URL}/health", timeout=2)
            if r.status_code != 200:
                alerts.append({"message": "Health service unhealthy", "timestamp": time.time()})
        except requests.RequestException:
            alerts.append({"message": "Health service unreachable", "timestamp": time.time()})
        time.sleep(POLL_INTERVAL)


@app.route("/health")
def health():
    return jsonify({"status": "UP"})


@app.route("/version")
def version():
    return jsonify({"version": "1.0.0"})


@app.route("/alerts")
def get_alerts():
    return jsonify(list(alerts))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    threading.Thread(target=poll_health, daemon=True).start()
    app.run(host="0.0.0.0", port=port)