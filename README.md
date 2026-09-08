# System Health Platform

## Services

- **health-service** (port 5000) - exposes `/health`, `/ready`, `/version`, `/environment`, `/dependencies`, `/history`.
- **metrics-service** (port 5001) - exposes `/health`, `/metrics` (Prometheus format, real CPU usage via psutil).
- **notifier-service** (port 5002) - exposes `/health`, `/alerts`; polls health-service every `POLL_INTERVAL_SECONDS` and records an alert when it becomes unreachable.