# Git workflow: 2+ branches and an explicit merge commit

```bash
cd flask-task-management-api
git init
git branch -M main
git remote add origin https://github.com/ShreyaRatnakar26/flask-task-management-api.git

# 1) Initial commit on main (core app)
git add app run.py requirements.txt requirements-dev.txt .gitignore README.md
git commit -m "feat: initial Flask task API"
git push -u origin main

# 2) Feature branch: tests + build tool
git checkout -b feature/tests-and-build
git add tests pyproject.toml Makefile
git commit -m "test: add pytest unit tests and build config"
git push -u origin feature/tests-and-build

# 3) Feature branch: CI (Jenkins + GitHub Actions)
git checkout -b feature/ci-pipeline
git add Jenkinsfile .github
git commit -m "ci: add Jenkinsfile and GitHub Actions workflow"
git push -u origin feature/ci-pipeline

# 4) Feature branch: Docker, Ansible, Kubernetes
git checkout -b feature/devops-deploy
git add Dockerfile .dockerignore ansible k8s GIT_COMMANDS.md
git commit -m "feat: add Docker, Ansible role, Kubernetes manifests"
git push -u origin feature/devops-deploy

# 5) Merge with explicit merge commits (--no-ff is important!)
git checkout main
git merge --no-ff feature/tests-and-build -m "Merge feature/tests-and-build into main"
git merge --no-ff feature/ci-pipeline -m "Merge feature/ci-pipeline into main"
git merge --no-ff feature/devops-deploy -m "Merge feature/devops-deploy into main"
git push origin main

# 6) Verify graph
git log --oneline --graph --all
```
