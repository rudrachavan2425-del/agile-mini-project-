# 🎓 CampusNexus - Online Placement System & End-to-End DevOps Pipeline

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1-black?logo=flask)](https://flask.palletsprojects.com/)
[![Tests](https://img.shields.io/badge/PyTest-16%20Passed-brightgreen?logo=pytest)](https://pytest.org)
[![Docker](https://img.shields.io/badge/Docker-Multi--Container-2496ED?logo=docker)](https://docker.com)
[![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?logo=jenkins)](https://jenkins.io)
[![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-E6522C?logo=prometheus)](https://prometheus.io)
[![Grafana](https://img.shields.io/badge/Grafana-Dashboards-F46800?logo=grafana)](https://grafana.com)

An enterprise-grade **Online Placement Management System** integrated with a complete **End-to-End DevOps CI/CD Pipeline**, designed strictly in accordance with **Mini-Project Experiment 10: End-to-End DevOps Pipeline**.

---

## 🌟 Key Application Features

1. **Recruitment Drives Catalog**:
   - Live corporate hiring drives (Google, Microsoft, Amazon, Goldman Sachs, Deloitte, Oracle, TCS Digital).
   - Package (CTC), minimum CGPA, eligible branches, location, and application deadline tracking.
   - Dynamic search, branch filtering (CSE, IT, ECE, EE, MECH, CIVIL), and status filters.

2. **Student Portal & Multi-Stage Application Tracking**:
   - Enrolled student profiles with cumulative CGPA, tech stack skills, and placement offers.
   - 1-Click application submission with real-time CGPA eligibility verification.
   - Status pipeline management: `Applied` &rarr; `Test Scheduled` &rarr; `Technical Round` &rarr; `HR Round` &rarr; `Selected (Offer)` &rarr; `Rejected`.

3. **Modern Glassmorphic Dark UI**:
   - Ultra-modern dark theme with ambient glowing radial mesh backgrounds.
   - Interactive visual charts (Chart.js) for branch-wise placement breakdown and applicant funnel.
   - Glowing metric highlight cards for placement rate, average package, and total drives.

4. **Built-in SRE & Chaos Simulator (Viva Demo Feature)**:
   - Live system telemetry (Host CPU %, Memory %, App State).
   - ⚡ **"Simulate CPU Spike (> 80%)"** button to trigger the Prometheus/Grafana `HighCPUUsage` alert.
   - ⚠️ **"Simulate HTTP 500 Error Spike"** button to trigger the `HighHttpErrorRate` alert.
   - 🛑 **"Toggle App Health"** button to trigger the `AppDown` alert rule immediately for examiner evaluation.

---

## 🔄 Complete DevOps CI/CD Architecture

```
Developer
    │
    ▼ Write Code
Git Repository
    │
    ▼ git push
GitHub
    │
    ▼ Webhook Trigger
Jenkins CI/CD Pipeline
    ├── Stage 1: Checkout Source Code
    ├── Stage 2: Install Dependencies (pip install -r requirements.txt)
    ├── Stage 3: Build & Static Analysis (py_compile)
    ├── Stage 4: Automated Testing (PyTest: 16 test cases pass)
    │             └── [FAIL → Stop Pipeline (Do not deploy!)]
    ├── Stage 5: Docker Build (Dockerfile)
    ├── Stage 6: Docker Push (Docker Hub)
    └── Stage 7: Deploy (Container running on port 5000)
    │
    ▼
Running Application (:5000)
    │
    ▼ Scrape /metrics every 5s
Prometheus Monitoring (:9090)
    │
    ▼ Visualize Metrics
Grafana Dashboard (:3000)
    │
    ▼ Trigger Abnormal Conditions
Alerting (CPU > 80% / App DOWN)
```

---

## 🚀 Quick Start Guide

### Option 1: Run Locally with Python

1. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run automated test suite**:
   ```bash
   pytest -v test_app.py
   ```
   *(All 16 tests pass!)*

3. **Start the application**:
   ```bash
   python app.py
   ```
   Open your browser at: **`http://localhost:5000`**

---

### Option 2: Run with Docker Compose (Full DevOps Stack)

Launch the Flask app, Prometheus, Grafana, and Node Exporter with a single command:

```bash
docker compose up -d --build
```

### 🌐 Service Endpoints

| Service | URL | Credentials / Notes |
| :--- | :--- | :--- |
| **Placement Portal** | [http://localhost:5000](http://localhost:5000) | Public Web Portal |
| **Health Check** | [http://localhost:5000/health](http://localhost:5000/health) | JSON Health status |
| **Prometheus Metrics**| [http://localhost:5000/metrics](http://localhost:5000/metrics) | Scraped by Prometheus |
| **DevOps SRE Cockpit**| [http://localhost:5000/devops](http://localhost:5000/devops) | Live telemetry & chaos testing |
| **Prometheus Server** | [http://localhost:9090](http://localhost:9090) | Targets & queries |
| **Prometheus Alerts** | [http://localhost:9090/alerts](http://localhost:9090/alerts) | Configured alert rules |
| **Grafana Dashboards**| [http://localhost:3000](http://localhost:3000) | User: `admin`, Pass: `admin` |
| **Node Exporter** | [http://localhost:9100](http://localhost:9100) | Host system metrics |

---

## 🧪 Automated Testing (`test_app.py`)

Before any deployment, automated testing executes:

```bash
python -m pytest -v test_app.py
```

### Test Suite Coverage:
- `test_home_page`: HTTP 200 and portal rendering.
- `test_drives_listing_page`: Catalog rendering and company listings.
- `test_drives_filter_by_branch`: Branch filtering query verification.
- `test_drive_detail_page`: Specific drive page and details.
- `test_add_new_drive`: Creating new placement drives via POST.
- `test_apply_drive_success`: Candidate application with qualifying CGPA.
- `test_apply_drive_ineligible_cgpa`: Rejection when candidate CGPA is below threshold.
- `test_update_application_status`: Progressing candidate across interview rounds.
- `test_health_endpoint`: JSON status schema on `/health`.
- `test_metrics_endpoint`: Prometheus text exposition format validation.
- `test_devops_panel`: SRE lab rendering.
- `test_chaos_error_spike_api`: Chaos injection endpoint testing.

---

## 🎯 Viva Demonstration Walkthrough (PDF Steps 1 to 12)

| Step | Action | Command / Location |
| :---: | :--- | :--- |
| **Step 1 & 2** | Modify code and push | `git commit -am "update"` && `git push` |
| **Step 3** | Webhook triggers Jenkins | Open `http://localhost:8080`, view active build |
| **Step 4** | Jenkins builds application | `Stage 3: Build` &rarr; SUCCESS |
| **Step 5** | Automated tests execute | `Stage 4: Automated Testing` &rarr; 16 PASSED |
| **Step 6** | Docker image created | `Stage 5: Docker Build` &rarr; `placement-app:latest` |
| **Step 7** | Docker image pushed | `Stage 6: Docker Push` &rarr; Docker Hub |
| **Step 8** | Application deployed | Container running on port 5000 |
| **Step 9** | Open application | Visit `http://localhost:5000` |
| **Step 10** | View metrics in Grafana | Visit `http://localhost:3000` &rarr; view CPU, Memory, HTTP rates |
| **Step 11** | **Generate alert condition** | Go to `http://localhost:5000/devops`, click **"Trigger CPU Load (> 80%)"** or **"Toggle App Health"** |
| **Step 12** | **Show fired alert** | Go to `http://localhost:9090/alerts`, observe `HighCPUUsage` or `AppDown` state change to **FIRING** (Red)! |

---

## 📂 Project Repository Structure

```
placement-management-devops/
│
├── app.py                      # Core Flask web application & Prometheus instrumentation
├── requirements.txt            # Python dependencies (Flask, PyTest, Prometheus, Psutil)
├── test_app.py                 # Automated unit and API test suite (16 tests)
├── Dockerfile                  # Production container definition
├── docker-compose.yml          # 4-Service multi-container orchestration
├── Jenkinsfile                 # 7-Stage declarative CI/CD pipeline
├── README.md                   # Comprehensive project documentation
├── PROJECT_REPORT.md           # 20-Section formal lab project report
├── SCREENSHOTS_GUIDE.md        # Step-by-step viva screenshot checklist
│
├── templates/                  # Jinja2 HTML Templates
│   ├── base.html               # Glassmorphic layout, navbar & status indicator
│   ├── index.html              # Analytics dashboard with Chart.js
│   ├── drives.html             # Placement drives directory with modal apply
│   ├── drive_detail.html       # Drive requirements & applicants pipeline
│   ├── add_drive.html          # Register new corporate drive
│   ├── students.html           # Candidate database with skills & status
│   ├── applications.html       # Application tracking board
│   └── devops_panel.html       # SRE Cockpit & Chaos Alert demonstration engine
│
├── static/                     # Assets & Design System
│   ├── css/
│   │   └── style.css           # Custom glassmorphic CSS design system
│   └── js/
│       └── main.js             # Client-side telemetry, animations & charts
│
├── prometheus/                 # Monitoring Configuration
│   ├── prometheus.yml          # Scrape configs for app and node-exporter
│   └── alert.rules.yml         # Prometheus alert rules (CPU > 80%, AppDown)
│
├── grafana/                    # Dashboard Provisioning
│   └── provisioning/
│       ├── datasources/
│       │   └── datasource.yml  # Auto-connects Prometheus datasource
│       └── dashboards/
│           ├── dashboards.yml  # Auto-loads dashboard provider
│           └── placement_devops_dashboard.json # Rich operational dashboard
│
└── jenkins/                    # Jenkins CI/CD Documentation
    └── setup_jenkins.md        # Detailed setup guide for Jenkins pipeline
```

---

## 📜 Laboratory Deliverables Checklist

- [x] Application source code with full functionality.
- [x] Automated test cases with PyTest (`test_app.py`).
- [x] Multi-stage `Dockerfile` and `docker-compose.yml`.
- [x] Declarative `Jenkinsfile` with 7 stages.
- [x] Prometheus metrics scraping and alerting rules (`alert.rules.yml`).
- [x] Grafana operational dashboard with CPU, Memory, Latency, and throughput panels.
- [x] Interactive chaos testing engine for viva alert demonstration.
- [x] 20-section formal mini-project report (`PROJECT_REPORT.md`).
- [x] Evidence screenshot guide (`SCREENSHOTS_GUIDE.md`).
