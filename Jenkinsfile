pipeline {
    agent any

    environment {
        REGISTRY = "docker.io/rishabh409"
        IMAGE = "${REGISTRY}/bookstore-app"
        TAG = "latest"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', credentialsId: 'github-creds', url: 'https://github.com/Rishabh-11-bit/bookstore-devops-pipeline.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $IMAGE:$TAG .'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                        sh 'docker push $IMAGE:$TAG'
                    }
                }
            }
        }
    }

    post {
        success {
            echo '✅ CI pipeline successful! Image pushed to Docker Hub.'
        }
        failure {
            echo '❌ Pipeline failed. Check build logs.'
        }
    }
}
