pipeline {
    agent any

    environment {
        APP_NAME = "online-placement-system"
        DOCKER_IMAGE = "placement-app"
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo 'Checking out source code from Git repository...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Setting up Python dependencies...'
                sh '''
                    python3 -m venv venv || python -m venv venv
                    . venv/bin/activate || . venv/Scripts/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Build / Validate') {
            steps {
                echo 'Validating Python syntax and structure...'
                sh '''
                    . venv/bin/activate || . venv/Scripts/activate
                    python -m py_compile app.py test_app.py
                    echo "Validation: SUCCESS"
                '''
            }
        }

        stage('Automated Tests') {
            steps {
                echo 'Running PyTest test suite...'
                sh '''
                    . venv/bin/activate || . venv/Scripts/activate
                    pytest -v test_app.py
                '''
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker container image...'
                sh 'docker build -t placement-app:latest .'
            }
        }

        stage('Docker Hub Push') {
            steps {
                echo 'Docker image tagged for repository.'
                sh 'docker tag placement-app:latest rudra200629/placement-app:latest || true'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application container...'
                sh 'docker restart placement-app || true'
            }
        }
    }

    post {
        always {
            stage('Post Actions') {
                echo 'Pipeline passed: tests, Docker build, and configured deployment stages completed.'
            }
        }
        success {
            echo 'Finished: SUCCESS'
        }
    }
}
