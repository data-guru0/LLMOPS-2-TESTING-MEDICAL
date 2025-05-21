pipeline{
    agent any

    // environment {
    //     SONAR_PROJECT_KEY = 'LLMOPS'
	// 	SONAR_SCANNER_HOME = tool 'Sonarqube'
    //     AWS_REGION = 'us-east-1'
    //     ECR_REPO = 'my-repo'
    //     IMAGE_TAG = 'latest'
	// }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/data-guru0/LLMOPS-2-TESTING-MEDICAL.git']])
                }
            }
        }

    stage('Comprehensive Trivy Scan') {
    steps {
        script {
            echo 'Running comprehensive Trivy scan (vuln + secrets + licenses)...'

            def reportFile = 'trivy-full-report.txt'

            // Run trivy filesystem scan with multiple scanners and severities
            // Using --scanners vuln,secret,license for full coverage
            // Scan entire workspace ('.'), fail on any HIGH or CRITICAL vuln
            sh """
                trivy fs \\
                    --exit-code 1 \\
                    --severity CRITICAL,HIGH,MEDIUM,LOW,UNKNOWN \\
                    --scanners vuln,secret,license \\
                    --no-progress \\
                    --format table \\
                    . | tee ${reportFile}
            """

            archiveArtifacts artifacts: reportFile, onlyIfSuccessful: true
        }
    }
}
    // stage('Build and Push Docker Image to ECR') {
    //         steps {
    //             withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
    //                 script {
    //                     def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
    //                     def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"

    //                     sh """
    //                     aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ecrUrl}
    //                     docker build -t ${env.ECR_REPO}:${IMAGE_TAG} .
    //                     docker tag ${env.ECR_REPO}:${IMAGE_TAG} ${ecrUrl}:${IMAGE_TAG}
    //                     docker push ${ecrUrl}:${IMAGE_TAG}
    //                     """
    //                 }
    //             }
    //         }
    //     }

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