# Garuda

Garuda aims to observe the cascading effect of interdependent containers in a Kubernetes. <br>
This repo is the Backend containing Rest APIs of this system.

### Abstract

Big organizations such as Google and Facebook have
thousands of microservices, databases, filesystems, and many
other interdependent systems running in a synchronized manner.
In such a complex system, if one of the systems crashes, it
becomes very difficult to identify the other affected systems that
might crash as a domino effect. Suppose Service A is dependent
on Database D, Service B is also dependent on D. In this scenario,
if D crashes, then both services A and B will also crash. If we
somehow know that crashing D would result in crashing both A
and B, we could take some precautionary measures before taking
any action that might crash D. In the real world, there are
thousands of interdependent systems and it is almost impossible
to spontaneously identify all the affected systems. We propose a
solution that would identify the cascading effect of any system
going down and alert the user beforehand, which would enable
the user to take appropriate actions and minimize the
repercussions. In this paper, we present a solution that keeps
track of the cascading effect of failing services in the Kubernetes
cluster and alerts users beforehand.

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
