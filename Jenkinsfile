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

    stage('Build, Scan, and Push Docker Image to ECR') {
    steps {
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
            script {
                def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
                def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"
                def imageFullTag = "${ecrUrl}:${IMAGE_TAG}"

                sh """
                aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ecrUrl}
                docker build -t ${env.ECR_REPO}:${IMAGE_TAG} .

                # Run Trivy scan, allow pipeline to continue regardless of result
                trivy image --severity HIGH,CRITICAL  --format json -o trivy-report.json ${env.ECR_REPO}:${IMAGE_TAG} || true

                docker tag ${env.ECR_REPO}:${IMAGE_TAG} ${imageFullTag}
                docker push ${imageFullTag}
                """

                archiveArtifacts artifacts: 'trivy-report.txt', allowEmptyArchive: true
            }
        }
    }
}
    stage('Update AWS App Runner Service') {
    steps {
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
            script {
                def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
                def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"
                def imageFullTag = "${ecrUrl}:${IMAGE_TAG}"

                def serviceArn = sh(script: "aws apprunner list-services --query \"ServiceSummaryList[?ServiceName=='llmops'].ServiceArn\" --output text", returnStdout: true).trim()

                echo "Updating App Runner service with new image..."
                sh """
                aws apprunner update-service \
                    --service-arn ${serviceArn} \
                    --source-configuration ImageRepository={ImageIdentifier=${imageFullTag},ImageRepositoryType=ECR,ImageConfiguration={Port=8501}}
                """
            }
        }
    }
}
    
        
    }
}