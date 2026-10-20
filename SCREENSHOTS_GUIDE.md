# Viva & Submission Screenshots Guide
## Experiment 10: End-to-End DevOps Pipeline

Follow this checklist to capture the exact screenshots required for your laboratory report and viva submission:

---

### 1. GitHub Screenshots
- [ ] **1.1 GitHub Repository Overview**: Show the repo landing page with project files (`app.py`, `Dockerfile`, `Jenkinsfile`, etc.).
- [ ] **1.2 Commit History**: Click on **Commits** showing meaningful commit history (e.g., `Initial commit`, `feat: add metrics and alerts`).
- [ ] **1.3 Source Code View**: Screenshot showing `app.py` or `Jenkinsfile` in GitHub code browser.

---

### 2. Automated Testing Screenshots
- [ ] **2.1 Test Execution in Terminal**: Run:
  ```bash
  python -m pytest -v test_app.py
  ```
  Capture terminal showing **16 passed in 2.94s** in bright green.
- [ ] **2.2 Test Source Code**: Screenshot of `test_app.py` showing `test_home_page()`, `test_apply_drive_success()`, `test_health_endpoint()`, etc.

---

### 3. Jenkins CI/CD Pipeline Screenshots
- [ ] **3.1 Pipeline Stage View**: Show all stages in green:
  - `Stage 1: Checkout`
  - `Stage 2: Install Dependencies`
  - `Stage 3: Build & Static Analysis`
  - `Stage 4: Automated Testing`
  - `Stage 5: Docker Build`
  - `Stage 6: Docker Push`
  - `Stage 7: Deploy`
- [ ] **3.2 Build Success Console Output**: Screenshot of the console log ending with:
  `Finished: SUCCESS`
- [ ] **3.3 Test Failure Quality Gate (Viva Bonus)**: Show Jenkins stopping at Stage 4 in RED when an assertion deliberately fails (proving *"Don't deploy if tests fail"*).

---

### 4. Docker Screenshots
- [ ] **4.1 Docker Images**: Run `docker images` showing `placement-app`, `prom/prometheus`, `grafana/grafana`.
- [ ] **4.2 Running Containers**: Run `docker ps` or Docker Desktop showing 4 active containers:
  - `placement-app` (Port 5000)
  - `prometheus` (Port 9090)
  - `grafana` (Port 3000)
  - `node-exporter` (Port 9100)

---

### 5. Application UI Screenshots
- [ ] **5.1 Home Dashboard**: Navigate to `http://localhost:5000` showing glowing metric cards, Chart.js branch doughnut chart, and application funnel.
- [ ] **5.2 Job Drives Directory**: Navigate to `http://localhost:5000/drives` showing Google, Microsoft, Amazon cards with branch badges and CTC.
- [ ] **5.3 Drive Details & Apply**: Click on Google or Microsoft showing requirements and the apply modal.
- [ ] **5.4 Candidate Directory**: `http://localhost:5000/students` showing student profiles.
- [ ] **5.5 Application Tracking Board**: `http://localhost:5000/applications` showing applicant status update dropdown.
- [ ] **5.6 SRE & Chaos Simulator Panel**: `http://localhost:5000/devops` showing live gauges and simulation buttons.

---

### 6. Prometheus Monitoring Screenshots
- [ ] **6.1 Targets Page**: Open `http://localhost:9090/targets` showing `placement-app (1/1 up)` in green.
- [ ] **6.2 Metrics Raw Endpoint**: Open `http://localhost:5000/metrics` showing Prometheus text exposition.
- [ ] **6.3 Query Execution**: In Prometheus Graph tab, run:
  ```promql
  sum(rate(flask_http_requests_total[1m]))
  ```
  or
  ```promql
  system_cpu_usage_percent
  ```
  Capture the resulting graph.

---

### 7. Grafana Dashboard Screenshots
- [ ] **7.1 Full Dashboard Overview**: Open `http://localhost:3000` showing **CampusNexus - Online Placement DevOps Dashboard**.
- [ ] **7.2 System Gauges**: Close-up of Host CPU % and Memory % gauges.
- [ ] **7.3 Traffic & Latency Panels**: Graphs of HTTP Request Rate and P95 Response Latency.
- [ ] **7.4 Business KPIs**: Placed candidates counter and average package CTC.

---

### 8. Alerting Screenshots (PDF Steps 11 & 12)
- [ ] **8.1 Configured Alert Rules**: Open `http://localhost:9090/alerts` showing rules:
  - `HighCPUUsage`
  - `AppDown`
  - `HighHttpErrorRate`
- [ ] **8.2 Triggered Alert**:
  - In `http://localhost:5000/devops`, click **"Trigger CPU Load (> 80%)"** or **"Toggle App Health (Simulate DOWN)"**.
  - Refresh `http://localhost:9090/alerts` and capture the alert state turning **FIRING (Red)**!
  - This provides concrete proof of an active, functioning alerting pipeline!
