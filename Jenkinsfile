pipeline {
    agent any
    environment {
        GITHUB_TOKEN = credentials('****') // Replace with your GitHub token credential ID
        GITHUB_REPO = 'https://github.com/f2015712/one-click-deploy' // Replace with your repository (e.g., user/repo)
        PR_NUMBER = env.CHANGE_ID // Jenkins environment variable for PR number
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Run Python Tests') {
            steps {
                script {
                    // Run Python tests and generate a JUnit XML report
                    sh 'pytest --junitxml=test-results.xml || true'
                }
            }
        }
        stage('Post Test Results to GitHub') {
            steps {
                script {
                    // Parse the test results
                    def testResults = readFile('test-results.xml')

                    // Build a comment body
                    def comment = """
                        **Automated Test Results**
                        ```
                        ${testResults}
                        ```
                    """

                    // Post comment to GitHub PR
                    sh """
                        curl -H "Authorization: token ${GITHUB_TOKEN}" \
                             -X POST \
                             -d '{ "body": "${comment}" }' \
                             https://api.github.com/repos/${GITHUB_REPO}/issues/${PR_NUMBER}/comments
                    """
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    sh 'docker build -t your-image-name:latest .'

                    // Optionally, push the image to a Docker registry
                    // sh 'docker push your-image-name:latest'
                }
            }
        }
    }
    post {
        always {
            // Publish test results in Jenkins
            junit 'test-results.xml'
        }
        
    }
}
