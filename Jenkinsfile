pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask-task-management-api'
    }

    triggers {
        // SCM polling fallback; also configure a GitHub webhook (see README)
        pollSCM('* * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_SHA = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements-dev.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '. venv/bin/activate && python -m pytest -v'
            }
        }

        stage('Build Package') {
            steps {
                sh '. venv/bin/activate && make package'
            }
        }

        stage('Docker Build (versioned)') {
            steps {
                // Tag reflects Jenkins build ID + Git SHA (Option B)
                sh 'docker build --build-arg APP_VERSION=${BUILD_NUMBER}-${GIT_SHA} -t ${IMAGE_NAME}:${BUILD_NUMBER}-${GIT_SHA} .'
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: 'dist/*', fingerprint: true
        }
    }
}
