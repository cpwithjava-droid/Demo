pipeline {
    agent any
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Build') { steps { sh 'mvn -B -DskipTests=false clean package' } }
        stage('SonarQube') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh "mvn sonar:sonar || true"
                }
            }
        }
        stage('Gitleaks') {
            steps { sh 'gitleaks detect --source . --report-path gitleaks-report.json || true' }
        }
        stage('Trivy') {
            steps { sh 'trivy fs --severity HIGH,CRITICAL --exit-code 1 . || true' }
        }
        stage('Deploy to UAT') {
            steps {
                sh 'cp target/*.jar ~/uat/ && ~/uat/deploy-uat.sh target/*.jar || true'
            }
        }
        stage('ZAP DAST') {
            steps {
                sh 'docker run --rm owasp/zap2docker-stable zap-baseline.py -t http://localhost:8080/hello -r zap-report.html || true'
            }
        }
        stage('Manual Approval') {
            steps { input message: "Deploy to Production?" }
        }
        stage('Deploy to PROD') {
            steps { sh 'cp target/*.jar ~/prod/ && ~/prod/deploy-prod.sh target/*.jar || true' }
        }
    }
}
