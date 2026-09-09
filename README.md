# System Health & Observability Platform

A microservices system built for the C456 SRE mini project: three cooperating Flask
services (health, metrics, notifier), containerised, deployed to a local Kubernetes
cluster, monitored with Prometheus and Grafana, and automated through a Jenkins
pipeline.

## Services

- **health-service** (port 5000) - exposes `/health`, `/ready`, `/version`, `/environment`, `/dependencies`, `/history`.
- **metrics-service** (port 5001) - exposes `/health`, `/version`, `/metrics` (Prometheus format, real CPU usage via psutil).
- **notifier-service** (port 5002) - exposes `/health`, `/version`, `/alerts`; polls health-service every `POLL_INTERVAL_SECONDS` and records an alert when it becomes unreachable.

## Prerequisites

- Python 3.11+
- Docker Desktop
- `kind` and `kubectl`
- Jenkins (local, running as a Windows service in this project)
- Git

## Run locally without Docker

Each service needs its own terminal window and its own `PORT` environment variable:

```powershell
cd services/health-service
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Repeat for `metrics-service` (`$env:PORT = "5001"` before `python app.py`) and
`notifier-service` (`$env:PORT = "5002"`).

## Run tests

```powershell
cd services/health-service
pytest tests/
```

Repeat for `metrics-service` and `notifier-service`. Each service has 2 tests; all
should pass independently.

## Run with Docker Compose

```powershell
docker compose up --build -d
curl.exe http://localhost:5000/dependencies
```

Expected result once all three containers are up: `{"metrics-service":"UP","notifier-service":"UP"}`.

## Deploy to Kubernetes (kind)

```powershell
kind create cluster --name health-platform

docker build -t system-health-platform-health-service:1.0 services/health-service
docker build -t system-health-platform-metrics-service:1.0 services/metrics-service
docker build -t system-health-platform-notifier-service:1.0 services/notifier-service

kind load docker-image system-health-platform-health-service:1.0 --name health-platform
kind load docker-image system-health-platform-metrics-service:1.0 --name health-platform
kind load docker-image system-health-platform-notifier-service:1.0 --name health-platform

kubectl apply -f k8s\health-service.yaml
kubectl apply -f k8s\metrics-service.yaml
kubectl apply -f k8s\notifier-service.yaml
kubectl apply -f k8s\monitoring\

kubectl get pods
```

Verify:
```powershell
kubectl port-forward svc/health-service 5020:5000
```
In a second window:
```powershell
curl.exe http://localhost:5020/dependencies
```

## Monitoring (Prometheus + Grafana)

```powershell
kubectl port-forward svc/prometheus 9091:9090
```
Check `http://localhost:9091/api/v1/targets` - `metrics-service` should show `"health":"up"`.

```powershell
kubectl port-forward svc/grafana 3001:3000
```
Open `http://localhost:3001`, log in, add `http://prometheus:9090` as a Prometheus
data source, and query `app_cpu_usage_percent` to see live CPU data plotted.

## CI/CD (Jenkins)

A local Jenkins instance (Windows service, `http://localhost:8080`) runs the pipeline
defined in `Jenkinsfile`. It checks out `develop`, installs dependencies, runs the full
test suite for all three services, builds and tags three Docker images with the build
number, loads them into the `kind` cluster, applies the Kubernetes manifests, waits for
successful rollout, and finishes with a live health check against the deployed
`health-service`. A failing test in the Install & Test stage stops the pipeline before
anything is built or deployed.

## Merge conflict

See `CONFLICT_NOTES.md` for a real merge conflict encountered (and resolved) on
`README.md` while merging `feature/notifier-service` into `develop`.

## AI assistance disclosure

This project was built with substantial AI assistance (Claude) for: initial project
scaffolding, Docker/Kubernetes/Jenkins configuration, and debugging environment issues
(PATH resolution, character encoding, Windows-specific shell syntax). All code was
reviewed, tested, and run personally; every bug encountered during setup was diagnosed
from real command output, not assumed fixed. See the conversation history for the full
debugging process, including several real issues found and fixed along the way
(missing service URLs in Docker Compose and Kubernetes deployments, a UTF-8 BOM
breaking Jenkins pipeline parsing, PATH/KUBECONFIG scoping differences between an
interactive user session and the Jenkins service account).