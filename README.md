# Flask Task Management API

REST API (Flask, in-memory storage) with a full DevOps pipeline: Git, Makefile/`python -m build`, Jenkins, GitHub Actions, Docker (multi-stage), Ansible, Kubernetes.

## Endpoints
| Method | Path | Description |
|---|---|---|
| GET | /health | Uptime / readiness |
| GET | /tasks | List tasks |
| POST | /tasks | Create task `{"title": "..."}` |
| GET | /tasks/<id> | Get one task |
| PUT | /tasks/<id> | Update task |
| DELETE | /tasks/<id> | Delete task |

## Run locally (VS Code terminal)
```bash
python -m venv venv
source venv/bin/activate          # Windows PowerShell: venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
python run.py                     # http://localhost:5000
```

## Test
```bash
python -m pytest -v
curl -i http://localhost:5000/health
curl -i -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d '{"title":"Learn Jenkins"}'
curl -i http://localhost:5000/tasks
```

## Build artifact (.whl / .tar.gz in dist/)
```bash
make package        # or: python -m build
```

## Docker
```bash
docker build -t flask-task-management-api:latest .
docker run -d -p 5000:5000 --name task-api flask-task-management-api:latest
docker images
```

## Ansible
```bash
cd ansible
ansible-playbook -i inventory playbook.yml
```

## Kubernetes (minikube)
```bash
minikube start
eval $(minikube docker-env)       # build image inside minikube
docker build -t flask-task-management-api:latest .
kubectl apply -f k8s/
kubectl get deployments,services,pods -o wide
minikube service flask-task-service --url
kubectl scale deployment flask-task-api --replicas=5
kubectl get pods
kubectl scale deployment flask-task-api --replicas=3
```
