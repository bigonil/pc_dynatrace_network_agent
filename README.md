# Dynatrace Network Observability Extension (Enterprise)

## Overview

This repository contains an **enterprise-grade network observability solution** built on **Dynatrace Extension Framework v2**, designed to monitor **network latency, jitter, packet loss, and connectivity quality** across **LAN, VPN, and Remote endpoints** on **Windows 11** devices.

The solution integrates natively with:
- Dynatrace SaaS
- ActiveGate
- Davis AI (automatic anomaly detection and RCA)
- Microsoft Intune (MSI-based mass rollout)

It is designed for **large enterprise environments (5,000+ endpoints)** with strict requirements on **security, scalability, governance, and automation**.

---

## Key Capabilities

- ICMP, TCP, and HTTP latency measurements
- Network jitter and packet loss calculation
- Execution via Dynatrace Extension v2 (Python runtime)
- ActiveGate-based centralized probing
- Endpoint-based probing for remote users
- Automatic baseline and anomaly detection (Davis AI)
- Alerting and RCA without custom ML pipelines
- Executive-ready dashboards
- Silent MSI installation
- Full Intune / GPO compatibility

---

## Target Architecture

### Execution Model

| Scenario | Execution Location |
|--------|--------------------|
| Corporate LAN | ActiveGate |
| VPN Users | ActiveGate |
| Remote / Home Users | Endpoint (Windows) |

### Data Flow

1. Network probes executed (Extension v2)
2. Metrics emitted via Dynatrace ingestion
3. Baselines automatically learned
4. Anomalies detected by Davis AI
5. Root cause correlated across:
   - Network
   - Host
   - Application
   - User Experience

---

## Repository Structure

```text
dynatrace-network-observability/
├── extension/
│   ├── extension.yaml
│   ├── activationSchema.json
│   ├── python/
│   │   ├── network_probe.py
│   │   ├── icmp.py
│   │   ├── tcp.py
│   │   ├── http.py
│   │   ├── jitter.py
│   │   ├── packet_loss.py
│   │   └── features.py
│   └── assets/icon.png
├── dashboards/
│   └── network_health_dashboard.json
├── installer/
│   ├── NetworkAgent.wxs
│   ├── install.ps1
│   └── uninstall.ps1
├── intune/
│   └── install.cmd
├── activegate/
│   └── deployment.md
├── playbook/
│   └── rollout_enterprise.md
└── README.md
