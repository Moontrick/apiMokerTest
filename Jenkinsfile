pipeline {
    agent any

    triggers {
        cron('0 8 * * *')
    }

    environment {
        PYTHONPATH = '.'
        PYTHON = 'C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Moontrick/apiMokerTest'
            }
        }

        stage('Install dependencies') {
            steps {
                bat '''
                    %PYTHON% -m venv venv
                    call venv\\Scripts\\activate.bat
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run tests') {
            steps {
                bat '''
                    call venv\\Scripts\\activate.bat
                    pytest -c pytest-ci.ini --alluredir=allure-results
                '''
            }
        }

        stage('Allure report') {
            steps {
                allure([
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'allure-results']]
                ])
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'logs\\**\\*', allowEmptyArchive: true
        }
        failure {
            echo 'Тесты упали — проверь Allure отчёт'
        }
    }
}