import os
import time
import math
import threading
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import psutil

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "placement-devops-secret-key-2026")

# ---------------------------------------------------------
# PROMETHEUS METRICS DEFINITIONS
# ---------------------------------------------------------
REQUEST_COUNT = Counter(
    "flask_http_requests_total",
    "Total HTTP request count",
    ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "flask_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["endpoint"]
)
GAUGE_DRIVES = Gauge("placement_drives_total", "Total registered placement drives")
GAUGE_APPLICATIONS = Gauge("placement_applications_total", "Total student applications submitted")
GAUGE_PLACED = Gauge("placement_placed_students_total", "Total students placed successfully")
GAUGE_AVG_CTC = Gauge("placement_avg_ctc_lpa", "Average CTC package in LPA")
GAUGE_CPU_PERCENT = Gauge("system_cpu_usage_percent", "System CPU usage percentage")
GAUGE_MEM_PERCENT = Gauge("system_memory_usage_percent", "System Memory usage percentage")
GAUGE_APP_HEALTH = Gauge("placement_app_health_status", "1 if app is healthy, 0 otherwise")

# Simulated health state (for DevOps alert testing)
SIMULATED_HEALTHY = True
SIMULATED_CPU_RUNNING = False

# ---------------------------------------------------------
# IN-MEMORY DATABASE WITH REALISTIC DATA
# ---------------------------------------------------------
DRIVES = [
    {
        "id": 1,
        "company": "Google",
        "role": "Software Development Engineer (SDE-1)",
        "ctc": 32.5,
        "min_cgpa": 8.5,
        "eligible_branches": ["CSE", "IT", "ECE"],
        "deadline": "2026-11-15",
        "drive_date": "2026-11-20",
        "location": "Bengaluru / Hyderabad",
        "status": "Active",
        "description": "Designing and building resilient large-scale distributed systems and core cloud infrastructure.",
        "logo_color": "#4285F4"
    },
    {
        "id": 2,
        "company": "Microsoft",
        "role": "Cloud Solutions & DevOps Engineer",
        "ctc": 28.0,
        "min_cgpa": 8.0,
        "eligible_branches": ["CSE", "IT", "ECE", "EE"],
        "deadline": "2026-11-18",
        "drive_date": "2026-11-22",
        "location": "Hyderabad / Noida",
        "status": "Active",
        "description": "Architecting Azure microservices, CI/CD pipelines, and enterprise cloud migration frameworks.",
        "logo_color": "#00A4EF"
    },
    {
        "id": 3,
        "company": "Amazon",
        "role": "Software Development Engineer (Backend)",
        "ctc": 26.5,
        "min_cgpa": 7.5,
        "eligible_branches": ["CSE", "IT", "ECE"],
        "deadline": "2026-11-20",
        "drive_date": "2026-11-25",
        "location": "Bengaluru / Pune",
        "status": "Active",
        "description": "Building high-throughput, low-latency transaction engines powering AWS and e-commerce platforms.",
        "logo_color": "#FF9900"
    },
    {
        "id": 4,
        "company": "Goldman Sachs",
        "role": "Quantitative Analyst & Platform Dev",
        "ctc": 24.0,
        "min_cgpa": 8.0,
        "eligible_branches": ["CSE", "IT", "ECE", "MECH"],
        "deadline": "2026-11-25",
        "drive_date": "2026-11-29",
        "location": "Bengaluru",
        "status": "Active",
        "description": "Developing mathematical pricing models and ultra-low latency algorithmic trading engines.",
        "logo_color": "#1E90FF"
    },
    {
        "id": 5,
        "company": "Oracle",
        "role": "Cloud Database Systems Engineer",
        "ctc": 19.5,
        "min_cgpa": 7.5,
        "eligible_branches": ["CSE", "IT"],
        "deadline": "2026-11-10",
        "drive_date": "2026-11-14",
        "location": "Bengaluru",
        "status": "In-Progress",
        "description": "Engineering autonomous database kernels, storage engines, and high-availability clustering.",
        "logo_color": "#F80000"
    },
    {
        "id": 6,
        "company": "Deloitte",
        "role": "Technology & Cybersecurity Consultant",
        "ctc": 12.0,
        "min_cgpa": 7.0,
        "eligible_branches": ["CSE", "IT", "ECE", "EE", "MECH", "CIVIL"],
        "deadline": "2026-12-05",
        "drive_date": "2026-12-12",
        "location": "Mumbai / Gurugram",
        "status": "Upcoming",
        "description": "Advising Fortune 500 clients on zero-trust cloud architectures, DevSecOps, and risk controls.",
        "logo_color": "#86BC25"
    },
    {
        "id": 7,
        "company": "TCS Digital",
        "role": "Systems Innovator & Full Stack Dev",
        "ctc": 7.5,
        "min_cgpa": 6.8,
        "eligible_branches": ["CSE", "IT", "ECE", "EE", "MECH", "CIVIL"],
        "deadline": "2026-12-10",
        "drive_date": "2026-12-18",
        "location": "Pan-India",
        "status": "Upcoming",
        "description": "Rapid digital prototyping, AI/ML integrations, and enterprise web application modernization.",
        "logo_color": "#502c84"
    }
]

STUDENTS = [
    {
        "id": 1,
        "name": "Aarav Sharma",
        "usn": "1MS21CS045",
        "email": "aarav.sharma@campus.edu",
        "branch": "CSE",
        "cgpa": 9.2,
        "skills": "Python, Go, Docker, Kubernetes, FastApi",
        "status": "Placed",
        "company": "Google",
        "package": 32.5
    },
    {
        "id": 2,
        "name": "Diya Patel",
        "usn": "1MS21IS028",
        "email": "diya.patel@campus.edu",
        "branch": "IT",
        "cgpa": 8.9,
        "skills": "Java, Spring Boot, AWS, Terraform, CI/CD",
        "status": "Placed",
        "company": "Microsoft",
        "package": 28.0
    },
    {
        "id": 3,
        "name": "Rohan Deshmukh",
        "usn": "1MS21EC082",
        "email": "rohan.d@campus.edu",
        "branch": "ECE",
        "cgpa": 8.4,
        "skills": "C++, Embedded Linux, ROS, Python, Git",
        "status": "Placed",
        "company": "Amazon",
        "package": 26.5
    },
    {
        "id": 4,
        "name": "Ananya Roy",
        "usn": "1MS21CS099",
        "email": "ananya.roy@campus.edu",
        "branch": "CSE",
        "cgpa": 8.7,
        "skills": "React, TypeScript, Node.js, PostgreSQL, Docker",
        "status": "Seeking",
        "company": None,
        "package": 0.0
    },
    {
        "id": 5,
        "name": "Karthik Subramanian",
        "usn": "1MS21EE034",
        "email": "karthik.s@campus.edu",
        "branch": "EE",
        "cgpa": 7.8,
        "skills": "Python, MATLAB, Power Systems, Linux",
        "status": "Seeking",
        "company": None,
        "package": 0.0
    },
    {
        "id": 6,
        "name": "Pooja Hegde",
        "usn": "1MS21ME051",
        "email": "pooja.h@campus.edu",
        "branch": "MECH",
        "cgpa": 7.4,
        "skills": "CAD, Python, Finite Element Analysis, Git",
        "status": "Seeking",
        "company": None,
        "package": 0.0
    }
]

APPLICATIONS = [
    {
        "id": 1,
        "drive_id": 1,
        "company": "Google",
        "student_name": "Aarav Sharma",
        "usn": "1MS21CS045",
        "branch": "CSE",
        "cgpa": 9.2,
        "status": "Selected",
        "applied_on": "2026-10-02 14:32"
    },
    {
        "id": 2,
        "drive_id": 2,
        "company": "Microsoft",
        "student_name": "Diya Patel",
        "usn": "1MS21IS028",
        "branch": "IT",
        "cgpa": 8.9,
        "status": "Selected",
        "applied_on": "2026-10-04 10:15"
    },
    {
        "id": 3,
        "drive_id": 3,
        "company": "Amazon",
        "student_name": "Rohan Deshmukh",
        "usn": "1MS21EC082",
        "branch": "ECE",
        "cgpa": 8.4,
        "status": "Selected",
        "applied_on": "2026-10-05 16:40"
    },
    {
        "id": 4,
        "drive_id": 1,
        "company": "Google",
        "student_name": "Ananya Roy",
        "usn": "1MS21CS099",
        "branch": "CSE",
        "cgpa": 8.7,
        "status": "Interview Scheduled",
        "applied_on": "2026-10-08 11:20"
    },
    {
        "id": 5,
        "drive_id": 4,
        "company": "Goldman Sachs",
        "student_name": "Ananya Roy",
        "usn": "1MS21CS099",
        "branch": "CSE",
        "cgpa": 8.7,
        "status": "Technical Round",
        "applied_on": "2026-10-12 09:30"
    },
    {
        "id": 6,
        "drive_id": 6,
        "company": "Deloitte",
        "student_name": "Karthik Subramanian",
        "usn": "1MS21EE034",
        "branch": "EE",
        "cgpa": 7.8,
        "status": "Applied",
        "applied_on": "2026-10-14 18:05"
    }
]

# Helper to calculate stats
def get_stats():
    total_drives = len(DRIVES)
    active_drives = sum(1 for d in DRIVES if d["status"] == "Active")
    total_students = len(STUDENTS)
    placed_students = sum(1 for s in STUDENTS if s["status"] == "Placed")
    placement_rate = round((placed_students / total_students * 100), 1) if total_students else 0.0
    packages = [s["package"] for s in STUDENTS if s["status"] == "Placed" and s["package"] > 0]
    avg_ctc = round(sum(packages) / len(packages), 2) if packages else 0.0
    max_ctc = max(packages) if packages else 0.0
    total_apps = len(APPLICATIONS)

    # Sync with Prometheus Gauges
    GAUGE_DRIVES.set(total_drives)
    GAUGE_APPLICATIONS.set(total_apps)
    GAUGE_PLACED.set(placed_students)
    GAUGE_AVG_CTC.set(avg_ctc)
    GAUGE_APP_HEALTH.set(1 if SIMULATED_HEALTHY else 0)

    try:
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        GAUGE_CPU_PERCENT.set(cpu)
        GAUGE_MEM_PERCENT.set(mem)
    except Exception:
        cpu, mem = 15.0, 42.0

    return {
        "total_drives": total_drives,
        "active_drives": active_drives,
        "total_students": total_students,
        "placed_students": placed_students,
        "placement_rate": placement_rate,
        "avg_ctc": avg_ctc,
        "max_ctc": max_ctc,
        "total_apps": total_apps,
        "cpu_percent": cpu,
        "mem_percent": mem,
        "is_healthy": SIMULATED_HEALTHY
    }

# ---------------------------------------------------------
# REQUEST HOOKS FOR METRICS & LATENCY
# ---------------------------------------------------------
@app.before_request
def start_timer():
    request._start_time = time.time()

@app.after_request
def record_metrics(response):
    if hasattr(request, "_start_time"):
        latency = time.time() - request._start_time
        endpoint = request.endpoint or "unknown"
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status=str(response.status_code)
        ).inc()
    return response

# ---------------------------------------------------------
# APPLICATION ROUTES
# ---------------------------------------------------------
@app.route("/")
def home():
    stats = get_stats()
    recent_drives = sorted(DRIVES, key=lambda x: x["id"], reverse=True)[:4]
    recent_apps = sorted(APPLICATIONS, key=lambda x: x["id"], reverse=True)[:5]
    return render_template("index.html", stats=stats, recent_drives=recent_drives, recent_apps=recent_apps)

@app.route("/drives")
def drives():
    branch_filter = request.args.get("branch", "").strip().upper()
    status_filter = request.args.get("status", "").strip()
    search_query = request.args.get("q", "").strip().lower()

    filtered = DRIVES
    if branch_filter and branch_filter != "ALL":
        filtered = [d for d in filtered if branch_filter in d["eligible_branches"] or "ALL" in d["eligible_branches"]]
    if status_filter and status_filter != "ALL":
        filtered = [d for d in filtered if d["status"].lower() == status_filter.lower()]
    if search_query:
        filtered = [d for d in filtered if search_query in d["company"].lower() or search_query in d["role"].lower()]

    stats = get_stats()
    return render_template("drives.html", drives=filtered, stats=stats, branch_filter=branch_filter, status_filter=status_filter, search_query=search_query)

@app.route("/drives/<int:drive_id>")
def drive_detail(drive_id):
    drive = next((d for d in DRIVES if d["id"] == drive_id), None)
    if not drive:
        flash("Drive not found!", "danger")
        return redirect(url_for("drives"))

    drive_apps = [a for a in APPLICATIONS if a["drive_id"] == drive_id]
    stats = get_stats()
    return render_template("drive_detail.html", drive=drive, applicants=drive_apps, stats=stats)

@app.route("/drives/add", methods=["GET", "POST"])
def add_drive():
    if request.method == "POST":
        company = request.form.get("company", "").strip()
        role = request.form.get("role", "").strip()
        ctc = float(request.form.get("ctc", 0.0))
        min_cgpa = float(request.form.get("min_cgpa", 6.0))
        branches = [b.strip().upper() for b in request.form.get("branches", "CSE,IT").split(",") if b.strip()]
        deadline = request.form.get("deadline", "2026-12-31")
        drive_date = request.form.get("drive_date", "2026-12-31")
        location = request.form.get("location", "Bengaluru")
        status = request.form.get("status", "Active")
        description = request.form.get("description", "Exciting full-time placement opportunity.")

        new_id = max([d["id"] for d in DRIVES], default=0) + 1
        new_drive = {
            "id": new_id,
            "company": company,
            "role": role,
            "ctc": ctc,
            "min_cgpa": min_cgpa,
            "eligible_branches": branches,
            "deadline": deadline,
            "drive_date": drive_date,
            "location": location,
            "status": status,
            "description": description,
            "logo_color": "#6366F1"
        }
        DRIVES.append(new_drive)
        flash(f"Drive for {company} registered successfully!", "success")
        return redirect(url_for("drives"))

    return render_template("add_drive.html")

@app.route("/drives/<int:drive_id>/delete", methods=["POST"])
def delete_drive(drive_id):
    global DRIVES, APPLICATIONS
    drive = next((d for d in DRIVES if d["id"] == drive_id), None)
    if drive:
        DRIVES = [d for d in DRIVES if d["id"] != drive_id]
        APPLICATIONS = [a for a in APPLICATIONS if a["drive_id"] != drive_id]
        flash(f"Drive for {drive['company']} was deleted.", "info")
    else:
        flash("Drive not found.", "warning")
    return redirect(url_for("drives"))

@app.route("/students")
def students():
    branch_filter = request.args.get("branch", "").strip().upper()
    status_filter = request.args.get("status", "").strip()

    filtered = STUDENTS
    if branch_filter and branch_filter != "ALL":
        filtered = [s for s in filtered if s["branch"] == branch_filter]
    if status_filter and status_filter != "ALL":
        filtered = [s for s in filtered if s["status"].lower() == status_filter.lower()]

    stats = get_stats()
    return render_template("students.html", students=filtered, stats=stats)

@app.route("/applications")
def applications():
    stats = get_stats()
    status_filter = request.args.get("status", "").strip()
    filtered = APPLICATIONS
    if status_filter and status_filter != "ALL":
        filtered = [a for a in filtered if a["status"].lower() == status_filter.lower()]
    return render_template("applications.html", applications=filtered, stats=stats)

@app.route("/apply/<int:drive_id>", methods=["POST"])
def apply_drive(drive_id):
    drive = next((d for d in DRIVES if d["id"] == drive_id), None)
    if not drive:
        flash("Drive not found!", "danger")
        return redirect(url_for("drives"))

    student_name = request.form.get("student_name", "").strip()
    usn = request.form.get("usn", "").strip()
    branch = request.form.get("branch", "CSE").strip().upper()
    cgpa = float(request.form.get("cgpa", 0.0))

    # Basic eligibility check
    if cgpa < drive["min_cgpa"]:
        flash(f"Eligibility error: CGPA ({cgpa}) is lower than minimum requirement ({drive['min_cgpa']}).", "danger")
        return redirect(url_for("drive_detail", drive_id=drive_id))

    new_app_id = max([a["id"] for a in APPLICATIONS], default=0) + 1
    new_app = {
        "id": new_app_id,
        "drive_id": drive_id,
        "company": drive["company"],
        "student_name": student_name,
        "usn": usn,
        "branch": branch,
        "cgpa": cgpa,
        "status": "Applied",
        "applied_on": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    APPLICATIONS.append(new_app)
    flash(f"Application submitted successfully for {drive['company']}!", "success")
    return redirect(url_for("drive_detail", drive_id=drive_id))

@app.route("/applications/<int:app_id>/status", methods=["POST"])
def update_application_status(app_id):
    new_status = request.form.get("status")
    app_record = next((a for a in APPLICATIONS if a["id"] == app_id), None)
    if app_record and new_status:
        app_record["status"] = new_status
        # If placed / selected, sync student record
        if new_status == "Selected":
            drive = next((d for d in DRIVES if d["id"] == app_record["drive_id"]), None)
            student = next((s for s in STUDENTS if s["usn"] == app_record["usn"]), None)
            if student and drive:
                student["status"] = "Placed"
                student["company"] = drive["company"]
                student["package"] = drive["ctc"]
        flash(f"Status for {app_record['student_name']} updated to {new_status}.", "success")
    return redirect(request.referrer or url_for("applications"))

# ---------------------------------------------------------
# DEVOPS, CHAOS TESTING & MONITORING ENDPOINTS
# ---------------------------------------------------------
@app.route("/devops")
def devops_panel():
    stats = get_stats()
    return render_template("devops_panel.html", stats=stats)

@app.route("/health")
def health_check():
    """Application health endpoint for Docker, Jenkins, and Prometheus."""
    if not SIMULATED_HEALTHY:
        return jsonify({
            "status": "DOWN",
            "message": "Simulated outage triggered for Alerting demo",
            "timestamp": datetime.now().isoformat()
        }), 503

    try:
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
    except Exception:
        cpu, mem = 10.0, 40.0

    return jsonify({
        "status": "UP",
        "service": "placement-management-system",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "database": "connected",
        "system": {
            "cpu_percent": cpu,
            "memory_percent": mem,
            "drives_count": len(DRIVES),
            "applications_count": len(APPLICATIONS)
        }
    }), 200

@app.route("/metrics")
def metrics():
    """Prometheus exposition format endpoint."""
    get_stats()
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route("/api/stats")
def api_stats():
    """JSON API for real-time dashboard UI charts."""
    stats = get_stats()
    branches = {}
    for s in STUDENTS:
        b = s["branch"]
        branches[b] = branches.get(b, 0) + (1 if s["status"] == "Placed" else 0)

    stages = {}
    for a in APPLICATIONS:
        st = a["status"]
        stages[st] = stages.get(st, 0) + 1

    return jsonify({
        "stats": stats,
        "branch_placements": branches,
        "application_stages": stages,
        "cpu": stats["cpu_percent"],
        "memory": stats["mem_percent"]
    })

# --- VIVA / DEMO CHAOS GENERATORS ---
def _burn_cpu(duration=15):
    global SIMULATED_CPU_RUNNING
    SIMULATED_CPU_RUNNING = True
    start = time.time()
    # Burn CPU cycles using heavy mathematical ops
    while time.time() - start < duration:
        for _ in range(500000):
            _ = math.sqrt(12345.6789) * math.sin(987.654)
    SIMULATED_CPU_RUNNING = False

@app.route("/api/chaos/cpu-load", methods=["POST"])
def simulate_cpu_load():
    """Triggers high CPU usage to test Prometheus/Grafana alert (CPU > 80%)."""
    global SIMULATED_CPU_RUNNING
    if not SIMULATED_CPU_RUNNING:
        t = threading.Thread(target=_burn_cpu, args=(15,))
        t.daemon = True
        t.start()
        return jsonify({
            "status": "triggered",
            "message": "High CPU load thread started for 15s to trigger Grafana/Prometheus alert rule (CPU > 80%)."
        }), 200
    return jsonify({"status": "already_running", "message": "CPU stress test already active."}), 200

@app.route("/api/chaos/error-spike", methods=["POST"])
def simulate_error_spike():
    """Increments 500 status code count for alert testing."""
    for _ in range(15):
        REQUEST_COUNT.labels(method="GET", endpoint="/api/chaos/error-spike", status="500").inc()
    return jsonify({
        "status": "errors_generated",
        "message": "Generated 15 simulated HTTP 500 errors to test High Error Rate alert."
    }), 200

@app.route("/api/chaos/toggle-health", methods=["POST"])
def toggle_health():
    """Toggles simulated app down condition for Viva Alert demo."""
    global SIMULATED_HEALTHY
    SIMULATED_HEALTHY = not SIMULATED_HEALTHY
    state = "UP" if SIMULATED_HEALTHY else "DOWN"
    GAUGE_APP_HEALTH.set(1 if SIMULATED_HEALTHY else 0)
    return jsonify({
        "status": state,
        "message": f"Application health state changed to {state}. Prometheus & Grafana will detect this on next poll."
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Starting Online Placement Management System on http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
