pipeline {
  agent any

  environment {
    IMAGE_TAG = "${env.BUILD_NUMBER}"
    KIND = "C:\\Users\\lenovo\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Kubernetes.kind_Microsoft.Winget.Source_8wekyb3d8bbwe\\kind.exe"
    KUBECTL = "C:\\Program Files\\Docker\\Docker\\resources\\bin\\kubectl.exe"
    KUBECONFIG = "C:\\Users\\lenovo\\.kube\\config"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Install & Test') {
      steps {
        script {
          for (svc in ['health-service', 'metrics-service', 'notifier-service']) {
            dir("services/${svc}") {
              bat 'python -m venv venv'
              bat 'venv\\Scripts\\pip install -r requirements.txt'
              bat 'venv\\Scripts\\pytest tests/'
            }
          }
        }
      }
    }

    stage('Build Images') {
      steps {
        script {
          for (svc in ['health-service', 'metrics-service', 'notifier-service']) {
            bat "docker build -t system-health-platform-${svc}:${IMAGE_TAG} services/${svc}"
          }
        }
      }
    }

    stage('Load into kind cluster') {
      steps {
        script {
          for (svc in ['health-service', 'metrics-service', 'notifier-service']) {
            bat "\"${KIND}\" load docker-image system-health-platform-${svc}:${IMAGE_TAG} --name health-platform"
          }
        }
      }
    }

    stage('Deploy') {
      steps {
        bat "\"${KUBECTL}\" apply -f k8s\\health-service.yaml"
        bat "\"${KUBECTL}\" apply -f k8s\\metrics-service.yaml"
        bat "\"${KUBECTL}\" apply -f k8s\\notifier-service.yaml"
        bat "\"${KUBECTL}\" apply -f k8s\\monitoring\\"
        bat "\"${KUBECTL}\" rollout status deployment/health-service --timeout=90s"
        bat "\"${KUBECTL}\" rollout status deployment/metrics-service --timeout=90s"
        bat "\"${KUBECTL}\" rollout status deployment/notifier-service --timeout=90s"
      }
    }

    stage('Health Check') {
      steps {
        bat "start /B \"\" \"${KUBECTL}\" port-forward svc/health-service 5099:5000"
        bat 'ping -n 7 127.0.0.1 > nul'
        bat 'curl -f http://localhost:5099/health'
        bat 'curl -f http://localhost:5099/dependencies'
      }
    }
  }

  post {
    failure {
      echo 'Pipeline failed - check the Install & Test stage first; a failing test should stop the build here.'
    }
  }
}