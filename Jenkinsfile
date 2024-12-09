pipeline {
    agent any

    environment {
        GITHUB_TOKEN = credentials('github_pat')  // GitHub PAT as a Jenkins credential
        GITHUB_REPO = 'https://github.com/f2015712/one-click-deploy' // Replace with your GitHub repository
    }
    triggers {
        // Automatically triggers on PR open or update events
        githubPullRequest {
            orgName('f2015712')
            repoName('one-click-deploy')
            triggerPhrase('retest')  // Optional: A command to manually trigger the build via comments
        }
    }

    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: 'main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/f2015712/one-click-deploy.git']]])
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    bash -c "source venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"
                '''
            }
        }
        stage('Build') {
            steps {
                sh '''
                    bash -c "source venv/bin/activate && python3 src/training.py"
                '''
            }
        }
        stage('Test') {
            steps {
                sh '''
                    bash -c "source venv/bin/activate && python3 -m pytest --maxfail=1 --disable-warnings --quiet --junitxml=test-results.xml"
                '''
            }
        }
        stage('Push Test Results to GitHub') {
            steps {
                script {
                    // Check if test-results.xml exists
                    def testResultsFile = 'test-results.xml'
                    if (fileExists(testResultsFile)) {
                        def testResults = sh(script: "cat ${testResultsFile}", returnStdout: true).trim()
                        def comment = """
                            **Automated Build and Test Results**
                            
                            Here are the results of the latest build and tests:
                            
                            ```
                            ${testResults}
                            ```
                        """
                        
                        // Posting the comment to the GitHub PR
                        if (env.CHANGE_ID) {
                            sh """
                                curl -H "Authorization: token ${GITHUB_TOKEN}" \
                                     -X POST \
                                     -d '{ "body": "${comment}" }' \
                                     https://api.github.com/repos/${GITHUB_REPO}/issues/${env.CHANGE_ID}/comments
                            """
                        } else {
                            echo 'No PR found. Skipping GitHub comment posting.'
                        }
                    } else {
                        echo 'Test results file not found. Skipping comment posting.'
                    }
                }
            }
        }
    }
    
    post {
        always {
            junit '**/test-results.xml' // Publish the test results in Jenkins
        }
    }
}
