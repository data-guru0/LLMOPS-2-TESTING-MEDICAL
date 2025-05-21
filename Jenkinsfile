pipeline{
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO = 'my-repo'
        IMAGE_TAG = 'latest'
	}

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/data-guru0/LLMOPS-2-TESTING-MEDICAL.git']])
                }
            }
        }

    
    stage('Build, Trivy Scan and Push Docker Image to ECR') {
    steps {
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
            script {
                def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
                def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"
                def imageName = "${env.ECR_REPO}:${IMAGE_TAG}"
                def fullImageName = "${ecrUrl}:${IMAGE_TAG}"
                def trivyImageReport = "trivy-image-report.txt"

                echo "🔨 Building Docker image..."
                sh "docker build -t ${imageName} ."

                echo "🔍 Scanning Docker image with Trivy..."
                sh """
                    trivy image \\
                        --exit-code 0 \\
                        --severity CRITICAL,HIGH,MEDIUM \\
                        --format table \\
                        --no-progress \\
                        ${imageName} | tee ${trivyImageReport}
                """

                archiveArtifacts artifacts: trivyImageReport, onlyIfSuccessful: true

                echo "🔐 Logging in to AWS ECR..."
                sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ecrUrl}"

                echo "🏷️ Tagging and pushing image to ECR..."
                sh """
                    docker tag ${imageName} ${fullImageName}
                    docker push ${fullImageName}
                """
            }
        }
    }
}
    //     stage('Deploy to ECS Fargate') {
    // steps {
    //     withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
    //         script {
    //             sh """
    //             aws ecs update-service \
    //               --cluster multi-ai-agent-cluster \
    //               --service multi-ai-agent-def-service-shqlo39p  \
    //               --force-new-deployment \
    //               --region ${AWS_REGION}
    //             """
    //             }
    //         }
    //     }
    //  }
        
    }
}