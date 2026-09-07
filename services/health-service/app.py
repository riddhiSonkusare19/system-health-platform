import os
import time
from collections import deque
from flask import Flask, jsonify
import requests

app = Flask(__name__)

APP_VERSION = "1.0.0"
ENVIRONMENT = os.environ.get("APP_ENVIRONMENT", "development")
METRICS_URL = os.environ.get("METRICS_SERVICE_URL", "http://localhost:5001")
NOTIFIER_URL = os.environ.get("NOTIFIER_SERVICE_URL", "http://localhost:5002")

health_history = deque(maxlen=20)


def record_check():
    entry = {"status": "UP", "timestamp": time.time()}
    health_history.append(entry)
    return entry


@app.route("/health")
def health():
    return jsonify(record_check())


@app.route("/ready")
def ready():
    return jsonify({"ready": True})


@app.route("/version")
def version():
    return jsonify({"version": APP_VERSION})


@app.route("/environment")
def environment():
    return jsonify({"environment": ENVIRONMENT})


@app.route("/dependencies")
def dependencies():
    deps = {}

    for name, url in [
        ("metrics-service", METRICS_URL),
        ("notifier-service", NOTIFIER_URL)
    ]:
        try:
            r = requests.get(f"{url}/health", timeout=2)
            deps[name] = "UP" if r.status_code == 200 else "DOWN"
        except requests.RequestException:
            deps[name] = "DOWN"

    return jsonify(deps)


@app.route("/history")
def history():
    return jsonify(list(health_history))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
