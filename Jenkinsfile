pipeline {
    agent any

    environment {
        APP_IMAGE = "simple-flask-app:${env.BUILD_NUMBER}"
        APP_URL = "http://localhost:5000"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/irfanriaz076/simple-flask-ci-cd.git'
            }
        }

        stage('Code Linting') {
            steps {
                sh '''
                    cd app
                    pip3 install -r requirements.txt --break-system-packages
                    flake8 .
                '''
            }
        }

        stage('Code Build') {
            steps {
                sh '''
                    docker build -t ${APP_IMAGE} .
                '''
            }
        }

        stage('Unit Testing') {
            steps {
                sh '''
                    # Ensure the workspace root (which contains the "app" package) is on PYTHONPATH
                    export PYTHONPATH="${WORKSPACE}"
                    cd ${WORKSPACE}
                    pytest tests/test_unit.py
                '''
            }
        }

        stage('Containerized Deployment') {
            steps {
                sh '''
                    docker rm -f simple-flask-container || true
                    docker run -d --name simple-flask-container -p 5000:5000 ${APP_IMAGE}
                    echo "Waiting for app to start..."
                    sleep 10
                '''
            }
        }

        stage('Selenium Testing') {
            steps {
                sh '''
                    export PYTHONPATH="${WORKSPACE}"
                    export APP_URL=${APP_URL}
                    cd ${WORKSPACE}
                    pytest tests/test_selenium.py
                '''
            }
        }
    }

    post {
        always {
            sh '''
                docker rm -f simple-flask-container || true
            '''
        }
    }
}
