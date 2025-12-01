# CloudFlowStocks Pipeline

Repo for the DevOps final: static site showing stock performance + insights built from Kaggle dataset and deployed via Jenkins → DigitalOcean.

See docs for instructions. Key components:
- Backend: FastAPI (reads processed dataset)
- Frontend: React (static)
- CI/CD: Jenkins (pipeline in Jenkinsfile)
- Reverse docs: Pyreverse + Graphviz (UML images embedded in LaTeX)
- Deployment: Docker Compose on DigitalOcean (domain: cloudflowstocks.me)
- Monitoring: Prometheus + Grafana

Follow the README sections for local demo and Jenkins setup.

*Please note: README is not finished