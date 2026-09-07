import os
import random
from flask import Flask, Response, jsonify

app = Flask(__name__)

ENVIRONMENT = os.environ.get("APP_ENVIRONMENT", "development")


@app.route("/health")
def health():
    return jsonify({"status": "UP"})


@app.route("/metrics")
def metrics():
    cpu = random.uniform(5, 80)
    mem = random.uniform(20, 90)
    req_count = random.randint(100, 5000)

    body = (
        "# HELP app_cpu_usage_percent Simulated CPU usage\n"
        "# TYPE app_cpu_usage_percent gauge\n"
        f"app_cpu_usage_percent {cpu:.2f}\n"
        "# HELP app_memory_usage_percent Simulated memory usage\n"
        "# TYPE app_memory_usage_percent gauge\n"
        f"app_memory_usage_percent {mem:.2f}\n"
        "# HELP app_requests_total Simulated total requests\n"
        "# TYPE app_requests_total counter\n"
        f"app_requests_total {req_count}\n"
    )

    return Response(body, mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
