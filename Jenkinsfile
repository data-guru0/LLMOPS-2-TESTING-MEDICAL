pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO = 'my-repo'
        IMAGE_TAG = "build-${BUILD_NUMBER}"
    }

    stages {
        stage('Cloning Github repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning GitHub repo to Jenkins...'
                    checkout scmGit(
                        branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'github-token',
                            url: 'https://github.com/data-guru0/LLMOPS-2-TESTING-MEDICAL.git'
                        ]]
                    )
                }
            }
        }

        stage('Build, Scan, and Push Docker Image to ECR') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
                    script {
                        def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
                        def ecrUrl = "${accountId}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"
                        def imageFullTag = "${ecrUrl}:${IMAGE_TAG}"

                        sh """
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ecrUrl}
                        docker build -t ${ECR_REPO}:${IMAGE_TAG} .
                        trivy image --severity HIGH,CRITICAL --format json -o trivy-report.json ${ECR_REPO}:${IMAGE_TAG} || true
                        docker tag ${ECR_REPO}:${IMAGE_TAG} ${imageFullTag}
                        docker push ${imageFullTag}
                        """
                        archiveArtifacts artifacts: 'trivy-report.json', allowEmptyArchive: true
                    }
                }
            }
        }

        stage('Deploy to Elastic Beanstalk') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
                    script {
                        def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
                        def ecrUrl = "${accountId}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}"

                        writeFile file: 'Dockerrun.aws.json', text: """
                        {
                          "AWSEBDockerrunVersion": 1,
                          "Image": {
                            "Name": "${ecrUrl}",
                            "Update": "true"
                          },
                          "Ports": [
                            {
                              "ContainerPort": 8501
                            }
                          ]
                        }
                        """

                        sh """
                        zip -r Dockerrun-${IMAGE_TAG}.zip Dockerrun.aws.json
                        aws s3 cp Dockerrun-${IMAGE_TAG}.zip s3://elasticbeanstalk-${AWS_REGION}-${accountId}/Dockerrun-${IMAGE_TAG}.zip

                        aws elasticbeanstalk create-application-version \
                          --application-name llmops \
                          --version-label ${IMAGE_TAG} \
                          --source-bundle S3Bucket=elasticbeanstalk-${AWS_REGION}-${accountId},S3Key=Dockerrun-${IMAGE_TAG}.zip

                        aws elasticbeanstalk update-environment \
                          --environment-name Llmops-env-1 \
                          --version-label ${IMAGE_TAG}
                        """
                    }
                }
            }
        }
    }
}
