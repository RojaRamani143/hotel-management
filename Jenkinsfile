pipeline {
    agent any
    environment {
        IMAGE_NAME = 'royalstay-hotel'
        CONTAINER_NAME = 'royalstay-container'
        HOST_PORT = '5000'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build image') {
            steps { sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .' }
        }
        stage('Deploy container') {
            steps {
                sh '''
                    docker volume create royalstay-data
                    docker rm -f ${CONTAINER_NAME} || true
                    docker run -d --name ${CONTAINER_NAME} \\
                      --restart unless-stopped \\
                      -p ${HOST_PORT}:5000 \\
                      -v royalstay-data:/app/data \\
                      -e SECRET_KEY="${SECRET_KEY:-demo-key-change-for-real-use}" \\
                      ${IMAGE_NAME}:${BUILD_NUMBER}
                '''
            }
        }
        stage('Health check') {
            steps {
                sh '''
                    for i in $(seq 1 15); do
                        if curl -fsS http://localhost:${HOST_PORT}/health; then
                            exit 0
                        fi
                        sleep 2
                    done
                    docker logs ${CONTAINER_NAME}
                    exit 1
                '''
            }
        }
    }
    post {
        success { echo 'RoyalStay deployed successfully!' }
        failure { echo 'Deployment failed. Review console output.' }
    }
}
