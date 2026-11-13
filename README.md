# Serverless Cloud Uptime Monitor

[![Serverless Uptime Check](https://github.com/mike-oluoch/web-uptime-monitor/actions/workflows/monitor.yml/badge.svg)](https://github.com/mike-oluoch/web-uptime-monitor/actions/workflows/monitor.yml)
![Python](https://img.shields.io/badge/Python-3.x%20Standard%20Library-blue)
![Hosting](https://img.shields.io/badge/Hosted%20on-GitHub%20Pages-22c55e)

A lightweight, zero-cost cloud monitoring system that automatically checks the availability and response latency of target web services every 15 minutes and publishes a live status dashboard on the web.

**Live Status Dashboard:** `https://mike-oluoch.github.io/web-uptime-monitor/`

---

## Overview

Traditional uptime monitors require provisioning a dedicated virtual private server (VPS) or paying for third-party SaaS subscriptions that run 24/7—even when idle between health checks. This project eliminates idle infrastructure by combining **ephemeral cloud compute** with **managed static web hosting**:

* **Automated Health Checks:** Pings configured HTTP/HTTPS endpoints on a recurring 15-minute schedule (or on demand) to verify reachability, capture HTTP status codes, and measure round-trip response latency in milliseconds.
* **Zero-Dependency Execution:** Built purely with Python's standard library (`urllib.request`, `time`, `json`, `datetime`), allowing cloud runners to execute checks in seconds without installing external packages.
* **Self-Updating Public Dashboard:** Persists telemetry in `status.json` and renders a responsive dark-mode status page via GitHub Pages with real-time `ONLINE` / `OFFLINE` indicators.

---

## Cloud & Virtualization Architecture

This system demonstrates three core cloud computing paradigms working together without persistent servers or external databases:

1. **Ephemeral Hardware Virtualization (GitHub Actions):** Every scheduled or manual run provisions a fresh, isolated `ubuntu-latest` virtual machine (4 vCPUs, 16 GB RAM, 14 GB SSD) hosted on cloud hypervisor infrastructure. Once `check.py` finishes, the VM is permanently destroyed.
2. **Git-Backed State Storage:** Instead of running a dedicated database instance, the cloud runner authenticates via a scoped `GITHUB_TOKEN` and commits updated telemetry directly to `status.json` in the repository.
3. **Managed PaaS / CDN Hosting (GitHub Pages):** Serves `index.html` and `status.json` globally over HTTPS, decoupling the front-end presentation layer from the back-end compute runner.

```text
[Cron Schedule (Every 15m) / Manual Workflow Dispatch]
                          │
                          ▼
┌───────────────────────────────────────────────────┐
│   GitHub Actions Runner (Ephemeral Ubuntu VM)     │
│   1. Checks out repository                        │
│   2. Executes check.py (HTTP GET + latency timer) │
│   3. Writes metrics to status.json                │
└─────────────────────────┬─────────────────────────┘
                          │ git commit & push [skip ci]
                          ▼
┌───────────────────────────────────────────────────┐
│   GitHub Repository (Versioned State Store)       │
│   • Stores updated status.json                    │
└─────────────────────────┬─────────────────────────┘
                          │ HTTPS GET (cache-busted fetch)
                          ▼
┌───────────────────────────────────────────────────┐
│   GitHub Pages (Managed Cloud Hosting)            │
│   • Serves live dashboard at *.github.io          │
└───────────────────────────────────────────────────┘
```

