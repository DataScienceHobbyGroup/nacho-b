
pipeline {
    options {
        buildDiscarder(logRotator(numToKeepStr: '10')) // Retain history on the last 10 builds
        timestamps() // Append timestamps to each line
        timeout(time: 20, unit: 'MINUTES') // Set a timeout on the total execution time of the job        
    }
    agent { label "nacho"}
    stages {   
        stage('Checkout') {
            steps {
                checkout scm
            }
        }     
        // stage("Linting") {
        //     steps {
        //         echo "Linting"
        //         sh "pip3 install pylint"
        //         sh "pylint *.py"
        //     }
        // }
        stage('Unit Testing') { // Perform unit testing
            steps {
                echo "Add testing"
                script {
                    sh """
                    pip install -r requirements.txt
                    """
                    sh """
                    python -m unittest discover -s tests/unit
                    """
                }
            }
        }
        // stage('Integration Testing') { //Perform integration testing
        //     steps {
        //         echo "add integration testing"
        //         // script {
        //         // sh """
        //         // # You have the option to stand up a temporary environment to perform
        //         // # these tests and/or run the tests against an existing environment. The
        //         // # advantage to the former is you can ensure the environment is clean
        //         // # and in a desired initial state. The easiest way to stand up a temporary
        //         // # environment is to use Docker and a wrapper script to orchestrate the
        //         // # process. This script will handle standing up supporting services like
        //         // # MySQL & Redis, running DB migrations, starting the web server, etc.
        //         // # You can utilize your existing automation, your custom scripts and Make.
        //         // ./standup_testing_environment.sh # Name this whatever you'd like
        //         // python -m unittest discover -s tests/integration
        //         // """
        //         // }
        //     }
        // }
        // stage('build') {
        //     steps {
        //         echo "Building ..."
        //     }
        // }
    }
    post {
        failure {
            script {
                msg = "Build error for ${env.JOB_NAME} ${env.BUILD_NUMBER} (${env.BUILD_URL})"
                
                echo msg
            }
        }
    }
}