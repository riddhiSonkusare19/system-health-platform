\# System Health Platform



\## Services



\- \*\*notifier-service\*\* (port 5002) — exposes `/health`, `/alerts`; polls health-service every `POLL\_INTERVAL\_SECONDS` and records an alert when it becomes unreachable.

