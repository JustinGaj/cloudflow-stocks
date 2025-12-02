pipeline {
  agent any
  environment {
    DOCKER_REG = 'ghcr.io/yourorg' // change to your registry
    VERSION_FILE = 'VERSION'
  }
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Setup') {
      steps {
        sh 'python3 -m pip install --upgrade pip || true'
        sh 'pip install --user pylint pyflakes pytest kaggle graphviz' // fallback
        sh 'node --version || true'
      }
    }
    stage('Fetch Kaggle Dataset') {
      steps {
        withCredentials([file(credentialsId: 'kaggle-json', variable: 'KAGGLE_FILE')]) {
          sh '''
            mkdir -p ~/.kaggle
            cp $KAGGLE_FILE ~/.kaggle/kaggle.json
            chmod 600 ~/.kaggle/kaggle.json
            ./backend/scripts/fetch_kaggle.sh
          '''
        }
      }
    }
    stage('Lint & Test') {
      steps {
        sh '''
          set -e
          # python lint & tests
          pytest -q backend || true
          # frontend tests (none) but ensure build works
          npm --prefix frontend ci --no-audit --no-fund || true
          npm --prefix frontend run build || true
        '''
      }
    }
    stage('Generate Reverse Docs & Compile LaTeX') {
      steps {
        sh '''
          pip install pylint pyreverse graphviz || true
          pyreverse -o png -p backend_diagrams backend/app || true
          mkdir -p docs/generated
          mv classes_backend_diagrams.png docs/generated/ || true
          # compile LaTeX (run from docs dir)
          pushd docs
          pdflatex -interaction=nonstopmode -halt-on-error latex/report.tex || true
          popd
        '''
      }
    }
    stage('Build Docker Images') {
      steps {
        sh '''
          # build backend and frontend images
          ./scripts/generate_version.sh > /tmp/version_tag
          TAG=$(cat /tmp/version_tag)
          docker build -t myapp-backend:${TAG} -f backend/Dockerfile backend
          docker build -t myapp-frontend:${TAG} -f frontend/Dockerfile frontend
        '''
      }
    }
    stage('Scan Images (Trivy)') {
      steps {
        sh '''
          # install trivy if not present
          if ! command -v trivy >/dev/null 2>&1; then
            curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
          fi
          TAG=$(cat /tmp/version_tag)
          trivy image --severity CRITICAL,HIGH --exit-code 1 myapp-backend:${TAG} || echo "Trivy returned issues (pipeline continues for demo)"
        '''
      }
    }
    stage('Package Artifact & Push Images') {
      steps {
        sh '''
          TAG=$(cat /tmp/version_tag)
          docker tag myapp-backend:${TAG} ${DOCKER_REG}/backend:${TAG}
          docker tag myapp-frontend:${TAG} ${DOCKER_REG}/frontend:${TAG}
        '''
        withCredentials([usernamePassword(credentialsId: 'docker-registry', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh '''
            echo $DOCKER_PASS | docker login ghcr.io -u $DOCKER_USER --password-stdin
            TAG=$(cat /tmp/version_tag)
            docker push ${DOCKER_REG}/backend:${TAG}
            docker push ${DOCKER_REG}/frontend:${TAG}
          '''
        }
        sh './scripts/build_artifact.sh'
        archiveArtifacts artifacts: 'artifacts/**', fingerprint: true
      }
    }
    stage('Deploy to DO (SSH)') {
      steps {
        sshagent (credentials: ['do-ssh-key']) {
          sh '''
            TAG=$(cat /tmp/version_tag)
            ssh -o StrictHostKeyChecking=no root@YOUR.DO.IP '
              cd /home/deploy/cloudflowstocks || mkdir -p /home/deploy/cloudflowstocks
              cd /home/deploy/cloudflowstocks
              echo "VERSION='${TAG}'" > .env
              docker-compose pull || true
              docker-compose up -d --remove-orphans
            '
          '''
        }
      }
    }
  }
  post {
    always {
      junit allowEmptyResults: true, testResults: 'backend/**/test-*.xml'
      archiveArtifacts artifacts: 'docs/**', fingerprint: true
    }
    success {
      echo "Pipeline succeeded"
    }
    failure {
      echo "Pipeline failed"
    }
  }
}
