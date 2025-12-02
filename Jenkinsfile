pipeline {
    agent any

    environment {
        // Docker image tag will include Jenkins build number
        APP_IMAGE = "simple-flask-app:${env.BUILD_NUMBER}"
        // URL where the app is reachable from the Jenkins agent
        APP_URL = "http://localhost:5000"
    }

    stages {
        stage('Checkout') {
            steps {
                // Adjust branch and repo URL if you use 'main' instead of 'master'
                git branch: 'master', url: 'https://github.com/irfanriaz076/simple-flask-ci-cd.git'
            }
        }

        stage('Code Linting') {
            steps {
                sh '''
                    cd app
                    # Install dependencies on Jenkins node
                    pip3 install -r requirements.txt --break-system-packages
                    flake8 .
                '''
            }
        }

        stage('Code Build') {
            steps {
                sh '''
                    # Build Docker image for the app
                    docker build -t ${APP_IMAGE} .
                '''
            }
        }

        stage('Unit Testing') {
            steps {
                sh '''
                    cd app
                    pytest ../tests/test_unit.py
                '''
            }
        }

        stage('Containerized Deployment') {
            steps {
                sh '''
                    # Stop old container if it exists
                    docker rm -f simple-flask-container || true

                    # Run new container from the built image
                    docker run -d --name simple-flask-container -p 5000:5000 ${APP_IMAGE}

                    echo "Waiting for app to start..."
                    sleep 10
                '''
            }
        }

        stage('Selenium Testing') {
            steps {
                sh '''
                    # APP_URL is set in environment; Selenium uses it
                    export APP_URL=${APP_URL}
                    cd app
                    pytest ../tests/test_selenium.py
                '''
            }
        }
    }

    post {
        always {
            sh '''
                # Clean up container after pipeline
                docker rm -f simple-flask-container || true
            '''
        }
    }
}
