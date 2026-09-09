pipeline {
    agent any

    environment {
        IMAGE_NAME = "system-health-dashboard"
        IMAGE_TAG  = "${IMAGE_NAME}:${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Checked out branch: ${GIT_BRANCH}"
            }
        }

        stage('Install') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                bat 'pytest tests/ -v'
            }
        }

        stage('Build') {
            steps {
                bat "docker build -t %IMAGE_TAG% ."
            }
        }

        stage('Tag') {
            steps {
                echo "Image tagged as: ${IMAGE_TAG}"
            }
        }

        stage('Health Check') {
            steps {
                bat "docker run -d -p 5001:5000 -e APP_ENV=ci --name health-check-container %IMAGE_TAG%"
                bat 'timeout /t 5 /nobreak'
                bat 'curl -f http://localhost:5001/health'
                bat 'docker stop health-check-container'
                bat 'docker rm health-check-container'
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed.'
        }
        success {
            echo 'Pipeline completed successfully.'
        }
    }
}
