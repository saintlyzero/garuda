# Garuda

Garuda aims to observe the cascading effect of interdependent containers in a Kubernetes. <br>
This repo is the Backend containing Rest APIs of this system.

### System Architecture

![System Architecture](assets/System%20Architecture.drawio.png)

### Cascading Effect Observation

#### Network Diagram with no failing service

![No Failure](assets/graph-1.jpg)

#### Network Diagram with failing service and their cascading effect

![No Failure](assets/graph-2.jpg)

##

Tech Stack

- FastAPI - Python
- Postgres
- D3.js
- Kubernetes
- Docker
- Prometheus
