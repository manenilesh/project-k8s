pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = "nileshmane912"
        IMAGE_NAME = "flask-redis-app"
        IMAGE_TAG = "${BUILD_NUMBER}"
        K8S_NAMESPACE = "flask-redis-demo"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t $DOCKERHUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG .
                    docker tag $DOCKERHUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG $DOCKERHUB_USERNAME/$IMAGE_NAME:latest
                '''
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                    docker push $DOCKERHUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG
                    docker push $DOCKERHUB_USERNAME/$IMAGE_NAME:latest
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f k8s/redis-deployment.yaml
                    kubectl apply -f k8s/flask-deployment.yaml
                    kubectl apply -f k8s/flask-service.yaml
                    kubectl rollout status deployment/flask-app -n $K8S_NAMESPACE
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    kubectl get pods -n $K8S_NAMESPACE
                    kubectl get svc -n $K8S_NAMESPACE
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully.'
        }
        failure {
            echo 'CI/CD pipeline failed. Check Jenkins console logs.'
        }
    }
}