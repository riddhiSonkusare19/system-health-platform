\# Stakeholder Update



\## Distributed System Health \& Observability Platform



\*\*Project Status:\*\* Near Complete

\*\*Current Stage:\*\* Documentation and Demo Preparation



\### 1. Project Overview



The Distributed System Health \& Observability Platform is an SRE-focused project designed to monitor the health of multiple services, expose operational metrics, detect service failures, and provide a foundation for automated deployment and monitoring.



The platform consists of three services:



\* \*\*Health Service\*\* – provides health, readiness, version, environment, dependency, and health-history endpoints.

\* \*\*Metrics Service\*\* – exposes application metrics in Prometheus format, including CPU usage, memory usage, and request count.

\* \*\*Notifier Service\*\* – monitors the Health Service and records alerts when the service becomes unavailable or unhealthy.

\* \*\*Gateway\*\* – provides a common entry point to the services.



\### 2. Current Progress



The major implementation stages have been completed:



\* Git repository and branching workflow

\* Three Flask-based services

\* Unit tests for the services

\* Intentional test failure demonstration

\* Git merge conflict creation and resolution

\* Pull request and review workflow

\* Dockerfiles for the services

\* Docker Compose deployment

\* Kubernetes deployment using kind

\* Gateway configuration

\* Prometheus monitoring

\* Grafana dashboard

\* Jenkins CI/CD pipeline

\* Pipeline failure and recovery demonstration

\* Project README and technical documentation



The repository is currently clean, with all committed changes synchronized with the remote `develop` branch.



\### 3. Key SRE Capabilities Demonstrated



The project demonstrates:



\* Service health monitoring

\* Dependency health checks

\* Automated failure detection

\* Prometheus-compatible metrics

\* Containerization with Docker

\* Kubernetes deployment and service discovery

\* CI/CD automation with Jenkins

\* Automated testing

\* Failure handling in the deployment pipeline

\* Git branching, pull requests, and conflict resolution

\* Operational documentation



\### 4. Remaining Work



The remaining work is primarily presentation and demonstration preparation:



1\. Final review of project documentation

2\. Verify the stakeholder update and RAID log

3\. Rehearse the complete 5-minute project demonstration

4\. Capture any final screenshots required as evidence



\### 5. RAID Log



| Type       | Item                                                                        | Impact                                                              | Action                                                               |

| ---------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------- |

| Risk       | Jenkins infrastructure or agent connectivity may become unavailable         | CI/CD demonstration could be interrupted                            | Verify Jenkins controller and Windows agent before the final demo    |

| Risk       | Docker/Kubernetes environment may behave differently between machines       | Deployment verification could fail during demonstration             | Run a complete end-to-end smoke test before the demo                 |

| Assumption | Required local tools such as Docker, kubectl, kind and Python are available | Project depends on the local development environment                | Verify tool versions before demonstration                            |

| Issue      | Local service ports required adjustment during development                  | Multiple Flask services initially attempted to use the same port    | Use configurable service ports and document the final configuration  |

| Dependency | Jenkins requires a working agent with Docker, kubectl and kind access       | Pipeline deployment depends on the agent environment                | Confirm agent connectivity and required tools                        |

| Decision   | Use Docker Compose for local multi-service verification                     | Provides a simple way to test service interaction before Kubernetes | Keep Compose configuration as the local integration test environment |



\### 6. Overall Status



\*\*Status: On Track\*\*



The core platform implementation is complete. The remaining focus is on documentation, final verification, and preparing a clear demonstration of the SRE workflow from source control through CI/CD, deployment, monitoring, and failure detection.



