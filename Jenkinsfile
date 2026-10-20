pipeline {
    agent any

    environment {
        APP_NAME = "online-placement-system"
        DOCKER_IMAGE = "placement-app"
        DOCKER_HUB_USER = credentials('dockerhub-username-id') // Or your Docker Hub username
        DOCKER_HUB_CREDS = credentials('dockerhub-credentials-id')
        REGISTRY = "docker.io"
        PORT = "5000"
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        ansiColor('xterm')
    }

    stages {
        // Stage 1: Checkout Source Code
        stage('Stage 1: Checkout') {
            steps {
                echo '📦 [Stage 1] Checking out source code from Git repository...'
                checkout scm
                script {
                    echo "Branch: ${env.BRANCH_NAME ?: 'main'}"
                    echo "Commit: ${env.GIT_COMMIT ?: 'HEAD'}"
                }
            }
        }

        // Stage 2: Install Dependencies
        stage('Stage 2: Install Dependencies') {
            steps {
                echo '🐍 [Stage 2] Setting up Python virtual environment & installing dependencies...'
                sh '''
                    python3 -m venv venv || python -m venv venv
                    . venv/bin/activate || . venv/Scripts/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        // Stage 3: Build & Static Analysis
        stage('Stage 3: Build & Static Analysis') {
            steps {
                echo '🔨 [Stage 3] Validating Python syntax & code structure...'
                sh '''
                    . venv/bin/activate || . venv/Scripts/activate
                    python -m py_compile app.py test_app.py
                    echo "Syntax compilation: SUCCESS"
                '''
            }
        }

        // Stage 4: Automated Testing (PyTest)
        stage('Stage 4: Automated Testing') {
            steps {
                echo '🧪 [Stage 4] Running PyTest test suite before deployment...'
                sh '''
                    . venv/bin/activate || . venv/Scripts/activate
                    pytest -v --junitxml=reports/test-results.xml test_app.py
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'reports/test-results.xml'
                }
                failure {
                    echo '❌ Automated tests FAILED! Aborting deployment pipeline.'
                }
            }
        }

        // Stage 5: Docker Build
        stage('Stage 5: Docker Build') {
            steps {
                echo '🐳 [Stage 5] Building container image...'
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} -t ${DOCKER_IMAGE}:latest ."
                }
            }
        }

        // Stage 6: Docker Push
        stage('Stage 6: Docker Push') {
            steps {
                echo '📤 [Stage 6] Pushing container image to Docker Hub repository...'
                script {
                    // In Jenkins with Docker Hub credentials:
                    /*
                    withDockerRegistry([credentialsId: 'dockerhub-credentials-id', url: '']) {
                        sh "docker tag ${DOCKER_IMAGE}:${BUILD_NUMBER} ${DOCKER_HUB_USER}/${DOCKER_IMAGE}:${BUILD_NUMBER}"
                        sh "docker tag ${DOCKER_IMAGE}:latest ${DOCKER_HUB_USER}/${DOCKER_IMAGE}:latest"
                        sh "docker push ${DOCKER_HUB_USER}/${DOCKER_IMAGE}:${BUILD_NUMBER}"
                        sh "docker push ${DOCKER_HUB_USER}/${DOCKER_IMAGE}:latest"
                    }
                    */
                    echo "Docker tag and push simulated: ${DOCKER_IMAGE}:${BUILD_NUMBER} -> Docker Hub"
                }
            }
        }

        // Stage 7: Deploy Containerized Application
        stage('Stage 7: Deploy') {
            steps {
                echo '🚀 [Stage 7] Deploying application container...'
                sh '''
                    # Stop any existing container
                    docker stop placement-app || true
                    docker rm placement-app || true
                    
                    # Run fresh container
                    docker run -d --name placement-app -p 5000:5000 --restart unless-stopped \
                        -e PORT=5000 -e SECRET_KEY=prod-secret-key-2026 ${DOCKER_IMAGE}:latest
                '''
                echo 'Waiting for application healthcheck on http://localhost:5000/health...'
                sh '''
                    sleep 5
                    curl -f http://localhost:5000/health || exit 1
                    echo "Deployment Verified: Application is Healthy and Running!"
                '''
            }
        }
    }

    // Post-Pipeline Actions & Notifications
    post {
        success {
            echo '🎉 ========================================================'
            echo '🎉 Jenkins CI/CD Pipeline Completed Successfully!'
            echo '🎉 Application deployed at: http://localhost:5000'
            echo '🎉 Prometheus metrics at:   http://localhost:5000/metrics'
            echo '🎉 Prometheus UI at:        http://localhost:9090'
            echo '🎉 Grafana Dashboard at:    http://localhost:3000'
            echo '🎉 ========================================================'
        }
        failure {
            echo '💥 ========================================================'
            echo '💥 Pipeline execution failed! Stopping pipeline.'
            echo '💥 Application was NOT deployed to prevent production outages.'
            echo '💥 ========================================================'
        }
    }
}
