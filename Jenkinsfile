pipeline {
    agent any

    environment {
        IMAGE_NAME = "sanchit69/cicd-flask-app"
        REGISTRY = "docker.io"
    }

    stages {

        stage('Clone') {
            steps {
                echo '📥 Cloning repository...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Running basic test...'
                sh """
                    docker run -d --name test-app-${BUILD_NUMBER} -p 5001:5000 ${IMAGE_NAME}:${BUILD_NUMBER}
                    sleep 3
                    curl -f http://localhost:5001 || exit 1
                    docker stop test-app-${BUILD_NUMBER} && docker rm test-app-${BUILD_NUMBER}
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
                        echo ${DOCKER_TOKEN} | docker login -u ${DOCKER_USER} --password-stdin
                        docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                        docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest
                        docker push ${IMAGE_NAME}:latest
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo '☸️ Deploying to Kubernetes...'
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBE_CONFIG')]) {
                    sh """
                        export KUBECONFIG=${KUBE_CONFIG}
                        sed -i '' 's|IMAGE_PLACEHOLDER|${IMAGE_NAME}:${BUILD_NUMBER}|g' k8s/deployment.yaml
                        kubectl apply -f k8s/deployment.yaml
                        kubectl apply -f k8s/service.yaml
                        kubectl rollout status deployment/flask-app
                    """
                }
            }
        }
    }

    post {
        success { echo '✅ Pipeline completed! App is live.' }
        failure { echo '❌ Pipeline failed. Check the logs above.' }
        always {
            sh "docker rmi ${IMAGE_NAME}:${BUILD_NUMBER} || true"
        }
    }
}
