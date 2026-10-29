pipeline {
    agent any
    environment {
        IMAGE   = 'nandakrishnanm/student-app'
        VERSION = "${env.BRANCH_NAME}"
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build Docker Image') {
            steps { bat 'docker build -t %IMAGE%:%VERSION% .' }
        }
        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
                    bat 'echo %DH_PASS%| docker login -u %DH_USER% --password-stdin'
                    bat 'docker push %IMAGE%:%VERSION%'
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                powershell '''
                $v = $env:VERSION
                $port = 30000 + [int]$v.Substring(1)
                (Get-Content k8s/app.yaml) -replace '__VERSION__',$v -replace '__PORT__',$port | Set-Content k8s/rendered.yaml
                kubectl apply -f k8s/rendered.yaml
                kubectl rollout restart deployment/student-app-$v
                kubectl rollout status deployment/student-app-$v --timeout=120s
                '''
            }
        }
    }
}