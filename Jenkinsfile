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
    
    stage('Deploy to Elastic Beanstalk') {
    steps {
        script {
            def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
            def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}:${IMAGE_TAG}"

            // Create Dockerrun.aws.json dynamically
            writeFile file: 'Dockerrun.aws.json', text: """
            {
              "AWSEBDockerrunVersion": 1,
              "Image": {
                "Name": "${ecrUrl}",
                "Update": "true"
              },
              "Ports": [
                {
                  "ContainerPort": "8501"
                }
              ]
            }
            """

            // Zip the file
            sh 'zip Dockerrun.zip Dockerrun.aws.json'

            // Upload and deploy
            sh """
            aws s3 cp Dockerrun.zip s3://elasticbeanstalk-us-east-1-254466556766/Dockerrun-${IMAGE_TAG}.zip

            aws elasticbeanstalk create-application-version \
              --application-name llmops \
              --version-label ${IMAGE_TAG} \
              --source-bundle S3Bucket=elasticbeanstalk-us-east-1-254466556766,S3Key=Dockerrun-${IMAGE_TAG}.zip || true

            aws elasticbeanstalk update-environment \
              --environment-name Llmops-env \
              --version-label ${IMAGE_TAG}
            """
        }
    }
}

    
        
    }
}