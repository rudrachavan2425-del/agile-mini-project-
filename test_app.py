import pytest
from app import app, DRIVES, APPLICATIONS, STUDENTS

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# -------------------------------------------------------------
# 1. CORE WEB PAGE TESTS
# -------------------------------------------------------------
def test_home_page(client):
    """Verifies that the home dashboard loads with status 200 and contains title."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Placement Management System" in response.data or b"Placement" in response.data

def test_drives_listing_page(client):
    """Verifies that the drives directory loads and displays active opportunities."""
    response = client.get("/drives")
    assert response.status_code == 200
    assert b"Google" in response.data
    assert b"Microsoft" in response.data

def test_drives_filter_by_branch(client):
    """Verifies branch filtering returns matching drives."""
    response = client.get("/drives?branch=CSE")
    assert response.status_code == 200
    assert b"Google" in response.data

def test_drive_detail_page(client):
    """Verifies that drive details page renders correctly for an existing drive."""
    response = client.get("/drives/1")
    assert response.status_code == 200
    assert b"Google" in response.data
    assert b"32.5" in response.data

def test_drive_detail_not_found(client):
    """Verifies redirect on invalid drive ID."""
    response = client.get("/drives/99999", follow_redirects=True)
    assert response.status_code == 200
    assert b"Drive not found" in response.data

def test_students_directory(client):
    """Verifies students directory lists enrolled candidates."""
    response = client.get("/students")
    assert response.status_code == 200
    assert b"Aarav Sharma" in response.data
    assert b"Diya Patel" in response.data

def test_applications_tracker(client):
    """Verifies applications tracking page."""
    response = client.get("/applications")
    assert response.status_code == 200
    assert b"Application" in response.data

# -------------------------------------------------------------
# 2. CRUD & BUSINESS LOGIC TESTS
# -------------------------------------------------------------
def test_add_new_drive(client):
    """Verifies creating a new placement drive via POST."""
    new_drive_data = {
        "company": "NVIDIA",
        "role": "AI/GPU Systems Engineer",
        "ctc": "35.0",
        "min_cgpa": "8.5",
        "branches": "CSE, IT, ECE",
        "deadline": "2026-12-15",
        "drive_date": "2026-12-20",
        "location": "Bengaluru",
        "status": "Active",
        "description": "Designing next-generation CUDA architecture and deep learning inference engines."
    }
    response = client.post("/drives/add", data=new_drive_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"NVIDIA" in response.data

def test_apply_drive_success(client):
    """Verifies student application with eligible CGPA."""
    app_data = {
        "student_name": "Test Candidate",
        "usn": "1MS21CS999",
        "branch": "CSE",
        "cgpa": "9.0"
    }
    response = client.post("/apply/1", data=app_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Application submitted successfully" in response.data

def test_apply_drive_ineligible_cgpa(client):
    """Verifies application rejection when CGPA is below drive requirement."""
    app_data = {
        "student_name": "Low CGPA Candidate",
        "usn": "1MS21CS001",
        "branch": "CSE",
        "cgpa": "6.0"  # Google requires 8.5
    }
    response = client.post("/apply/1", data=app_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Eligibility error" in response.data

def test_update_application_status(client):
    """Verifies status transition to Selected."""
    response = client.post("/applications/4/status", data={"status": "Selected"}, follow_redirects=True)
    assert response.status_code == 200
    # Check that status was updated
    app_item = next((a for a in APPLICATIONS if a["id"] == 4), None)
    assert app_item is not None
    assert app_item["status"] == "Selected"

# -------------------------------------------------------------
# 3. DEVOPS, METRICS & HEALTH API TESTS
# -------------------------------------------------------------
def test_health_endpoint(client):
    """Verifies that the /health endpoint returns HTTP 200 and JSON with UP status."""
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "UP"
    assert "service" in json_data
    assert "system" in json_data

def test_metrics_endpoint(client):
    """Verifies that /metrics returns Prometheus format metrics."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"flask_http_requests_total" in response.data
    assert b"system_cpu_usage_percent" in response.data
    assert b"placement_drives_total" in response.data

def test_devops_panel(client):
    """Verifies DevOps dashboard renders properly."""
    response = client.get("/devops")
    assert response.status_code == 200
    assert b"DevOps" in response.data

def test_api_stats(client):
    """Verifies live stats API for frontend charts."""
    response = client.get("/api/stats")
    assert response.status_code == 200
    json_data = response.get_json()
    assert "stats" in json_data
    assert "branch_placements" in json_data

def test_chaos_error_spike_api(client):
    """Verifies chaos error trigger for Prometheus alerting demo."""
    response = client.post("/api/chaos/error-spike")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "errors_generated"
