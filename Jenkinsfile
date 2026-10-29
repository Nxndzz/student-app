pipeline {
    agent any
    environment {
        IMAGE = "nandakrishnanm/student-app"
        TAG   = "${env.BRANCH_NAME}"
        DOCKERHUB = credentials('dockerhub-creds')
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build Docker Image') {
            steps { bat 'docker build -t %IMAGE%:%TAG% .' }
        }
        stage('Push to DockerHub') {
            steps {
                bat 'echo %DOCKERHUB_PSW%| docker login -u %DOCKERHUB_USR% --password-stdin'
                bat 'docker push %IMAGE%:%TAG%'
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f k8s/deployment.yaml'
                bat 'kubectl rollout restart deployment/student-app-%TAG%'
            }
        }
    }
}