# Jenkins CI/CD Setup Guide for Online Placement System

This guide explains how to set up, configure, and execute the Jenkins Continuous Integration and Continuous Deployment (CI/CD) pipeline for the **Campus Placement System**.

---

## 1. Running Jenkins via Docker

If you do not have Jenkins installed locally on Windows, you can spin it up with a single Docker command:

```bash
docker run -d \
  --name jenkins-server \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
```

### Unlocking Jenkins
1. Open your browser and navigate to `http://localhost:8080`
2. Retrieve the initial admin password:
   ```bash
   docker exec -it jenkins-server cat /var/jenkins_home/secrets/initialAdminPassword
   ```
3. Install **Suggested Plugins**.
4. Create your Admin user profile.

---

## 2. Required Jenkins Plugins

Ensure the following plugins are installed under **Manage Jenkins > Plugins**:
1. **Pipeline** (workflow-aggregator)
2. **Git Plugin**
3. **Docker Pipeline** & **Docker Plugin**
4. **HTML Publisher** (optional, for coverage reports)
5. **JUnit Plugin** (for test results visualization)

---

## 3. Configuring the Pipeline Job

1. From the Jenkins Dashboard, click **New Item**.
2. Enter item name: `placement-devops-pipeline`
3. Select **Pipeline** and click **OK**.
4. In the configuration page:
   - **Build Triggers**: Check **GitHub hook trigger for GITScm polling** (or Poll SCM `H/5 * * * *`).
   - Under **Pipeline Definition**:
     - Select **Pipeline script from SCM**
     - SCM: **Git**
     - Repository URL: `https://github.com/<your-username>/placement-management-devops.git`
     - Branch Specifier: `*/main`
     - Script Path: `Jenkinsfile`
5. Click **Save**.

---

## 4. Setting up GitHub Webhook for Automatic CI

To achieve **Push Code -> GitHub -> Webhook -> Jenkins -> Build**:
1. Go to your repository on GitHub.
2. Navigate to **Settings > Webhooks > Add webhook**.
3. Payload URL: `http://<your-jenkins-ip>:8080/github-webhook/`
4. Content type: `application/json`
5. Which events: Select **Just the push event**.
6. Click **Add webhook**.

---

## 5. Pipeline Stages Walkthrough

| Stage | Action | Success Criteria |
| :--- | :--- | :--- |
| **Stage 1: Checkout** | Clones code from GitHub repository | Repository fetched |
| **Stage 2: Dependencies** | Sets up virtualenv and runs `pip install -r requirements.txt` | Packages installed |
| **Stage 3: Build** | Validates syntax with `python -m py_compile` | No compilation errors |
| **Stage 4: Automated Testing** | Executes `pytest -v test_app.py` | 16/16 tests pass |
| **Stage 5: Docker Build** | Builds `Dockerfile` into container image | `docker build` code 0 |
| **Stage 6: Docker Push** | Tags and pushes image to Docker Hub | Image uploaded |
| **Stage 7: Deploy** | Restarts container with new image | `/health` returns 200 OK |

---

## 6. Viva Demonstration: Pipeline Failure Mode

To demonstrate the rule **"Don't deploy if tests fail"**:
1. Open `test_app.py` or `app.py`.
2. Change expected status code:
   ```python
   def test_home_page():
       response = client.get("/")
       assert response.status_code == 500  # Will fail!
   ```
3. Commit and push:
   ```bash
   git commit -am "test: introduce deliberate failure"
   git push origin main
   ```
4. Observe Jenkins: **Stage 4 fails in RED**, and **Stages 5, 6, and 7 are skipped**. The existing deployment remains untouched and secure!
