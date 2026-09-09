
from flask import Flask, jsonify, Response
import psutil
import os

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "UP"})


@app.route("/metrics", methods=["GET"])
def metrics():
    cpu_usage = psutil.cpu_percent(interval=0.1)

    metrics_data = f"""# HELP app_cpu_usage_percent Current application CPU usage
# TYPE app_cpu_usage_percent gauge
app_cpu_usage_percent {cpu_usage}
"""

    return Response(
        metrics_data,
        mimetype="text/plain"
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
