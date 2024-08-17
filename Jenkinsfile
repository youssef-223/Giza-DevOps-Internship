pipeline {
    agent any

    environment {
        GIT_REPO = 'https://github.com/youssef-223/Giza-DevOps-Internship.git'
        DOCKER_CREDENTIALS_ID = 'youssef223'
        GITHUB_CREDENTIALS_ID = 'my_github'
        WEBHOOK_URL = 'https://smee.io/RYBR63wIUrfdS1W'
        APP_IMAGE = 'youssef223/giza_project'
    }

    stages {

        stage('Listen to Webhook') {
            steps {
                script {
                    // Start the Smee webhook listener
                    sh """
                    nohup smee -u ${WEBHOOK_URL} -p 3000 > smee.log 2>&1 &
                    """
                }
            }
        }

        stage('Checkout') {
            steps {
                // Checkout the repository
                checkout([$class: 'GitSCM', branches: [[name: '*/master']], 
                          userRemoteConfigs: [[url: GIT_REPO, credentialsId: GITHUB_CREDENTIALS_ID]]])
            }
        }

        stage('Login to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://registry-1.docker.io', "${DOCKER_CREDENTIALS_ID}") {
                        // Docker login is handled by withRegistry
                    }
                }
            }
        }
        
        stage('Setup MySQL') {
            steps {
                script {
                    // Ensure the script is executable
                    sh 'chmod +x Scripts/mysql-install.sh'
                    // Run the MySQL installation script
                    sh 'Scripts/mysql-install.sh'
                }
            }
        }

        stage('Setup Database') {
            steps {
                script {
                    // Ensure the script is executable
                    sh 'chmod +x Scripts/mysql-setup.sh'
                    // Run the database setup script
                    sh 'Scripts/mysql-setup.sh'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image using the docker.build method
                    docker.build("${APP_IMAGE}:version_${env.BUILD_NUMBER}", "./app")
                }
            }
        }
        
        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://registry-1.docker.io', "${DOCKER_CREDENTIALS_ID}") {
                        // Push the Docker image with the tag version_${env.BUILD_NUMBER}
                        docker.image("${APP_IMAGE}:version_${env.BUILD_NUMBER}").push()
                        // Also push the image with the latest tag
                        docker.image("${APP_IMAGE}:version_${env.BUILD_NUMBER}").tag('latest')
                        docker.image("${APP_IMAGE}:latest").push()
                    }
                }
            }
        }

    }

    post {
        always {
            // Clean up any resources or perform actions that should always be done
            echo 'Pipeline completed.'
            cleanWs()
        }
        success {
            build job: 'Final-Project-CD', parameters: [string(name: 'BUILD_NUMBER', value: env.BUILD_NUMBER)]
        }
    }
}
