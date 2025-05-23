pipeline{
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO = 'my-repo'
        IMAGE_TAG = 'latest'
        CLUSTER_NAME = 'happy-country-unicorn'
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

    stage('Deploy to EKS') {
    steps {
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
            script {
                sh """
                aws eks --region ${AWS_REGION} update-kubeconfig --name ${CLUSTER_NAME}
                export KUBECONFIG=$HOME/.kube/config

                # Optional fix: skip validation if kubeconfig auth issue
                kubectl apply -f kubernetes-deployment.yaml --validate=false
                """
            }
        }
    }
}
        
    }
}