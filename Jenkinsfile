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
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'pytest tests/ -v'
            }
        }

        stage('Build') {
            steps {
                sh "docker build -t ${IMAGE_TAG} ."
                sh "docker images | grep ${IMAGE_NAME}"
            }
        }

        stage('Tag') {
            steps {
                echo "Image tagged as: ${IMAGE_TAG}"
            }
        }

        stage('Health Check') {
            steps {
                sh "docker run -d -p 5001:5000 -e APP_ENV=ci --name health-check-container ${IMAGE_TAG}"
                sh 'sleep 3'
                sh 'curl -f http://localhost:5001/health'
                sh 'docker stop health-check-container'
                sh 'docker rm health-check-container'
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed. Check the stage logs above.'
        }
        success {
            echo 'Pipeline completed successfully.'
        }
    }
}