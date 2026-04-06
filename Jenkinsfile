pipeline {
    agent any

    environment {
        PATH = "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
        IMAGE_NAME = "sanchit69/cicd-flask-app"
        REGISTRY = "docker.io"
        EC2_HOST = "13.49.246.189"
    }

    stages {

        stage('Clone') {
            steps {
                echo '📥 Cloning repository...'
                checkout scm
            }
        }

        stage('Check Docker') {
            steps {
                sh 'docker --version'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh """
                    docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                    docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest
                """
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Running basic test...'
                sh """
                    docker run -d --name test-app-${BUILD_NUMBER} -p 5002:9000 ${IMAGE_NAME}:${BUILD_NUMBER}
                    sleep 5
                    curl -f http://localhost:5002 || exit 1
                    docker stop test-app-${BUILD_NUMBER}
                    docker rm test-app-${BUILD_NUMBER}
                """
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo '📤 Pushing to Docker Hub...'
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_TOKEN'
                )]) {
                    sh """
                        echo "${DOCKER_TOKEN}" | docker login -u "${DOCKER_USER}" --password-stdin
                        docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                        docker push ${IMAGE_NAME}:latest
                    """
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                echo '🚀 Deploying to AWS EC2...'
                sshagent(['ec2-ssh-key']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ubuntu@${EC2_HOST} '
                        docker pull ${IMAGE_NAME}:latest &&
                        docker stop flask-app || true &&
                        docker rm flask-app || true &&
                        docker run -d --name flask-app -p 5000:9000 ${IMAGE_NAME}:latest
                        '
                    """
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed! App is live at http://13.49.246.189:5000'
        }

        failure {
            echo '❌ Pipeline failed. Check the logs above.'
        }

        always {
            sh """
                docker stop test-app-${BUILD_NUMBER} || true
                docker rm test-app-${BUILD_NUMBER} || true
                docker rmi ${IMAGE_NAME}:${BUILD_NUMBER} || true
            """
        }
    }
}