# System-Health-Dashboard

A lightweight REST API built for an operations team to expose basic system status information. The project covers the full delivery workflow — Git branching, automated testing, containerisation, and a Jenkins CI pipeline.

---

## Tech Stack

- Python 3.14 / Flask
- pytest
- Docker
- Jenkins
- Git / GitHub

---

## Prerequisites

Make sure the following are installed before you try to run anything.

- Python 3.8 or above
- pip
- Git
- Docker Desktop (must be running)
- Jenkins (local installation)

Verify each one:

```bash
python --version
pip --version
git --version
docker --version
```

---

## Project Structure

```
system-health-dashboard/
├── app.py
├── requirements.txt
├── pytest.ini
├── Dockerfile
├── .dockerignore
├── .gitignore
├── Jenkinsfile
├── README.md
└── tests/
    └── test_app.py
```

---

## Architecture

```
GitHub Repository
      |
      | (Pipeline script from SCM)
      v
Jenkins Pipeline
      |
      |-- Checkout   → pulls code from GitHub
      |-- Install    → pip install -r requirements.txt
      |-- Test       → pytest tests/ -v
      |-- Build      → docker build
      |-- Tag        → tags image with Jenkins build number
      |-- Health Check → runs container, curls /health endpoint
```

The application itself is a single Flask process exposing three endpoints. Configuration is read from environment variables so the same image runs in any environment without code changes.

---

## API Endpoints

| Endpoint | Response |
|---|---|
| /health | `{"status": "UP"}` |
| /version | `{"version": "1.1.0"}` |
| /environment | `{"environment": "<value of APP_ENV>"}` |

---

## Running Locally

Clone the repository:

```bash
git clone https://github.com/sahil070654/system-health-dashboard.git
cd system-health-dashboard
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
APP_ENV=development python app.py
```

The API will be available at `http://localhost:5000`.

Verify the endpoints:

```bash
curl http://localhost:5000/health
curl http://localhost:5000/version
curl http://localhost:5000/environment
```

---

## Running Tests

```bash
pytest tests/ -v
```

All three endpoint tests should pass. To see what a pipeline failure looks like, change the expected value in one test and run again, then revert.

---

## Running With Docker

Build the image:

```bash
docker build -t system-health-dashboard:1.0.0 .
```

Run the container with an environment variable:

```bash
docker run -p 5000:5000 -e APP_ENV=production system-health-dashboard:1.0.0
```

Verify the endpoints are responding from inside the container:

```bash
curl http://localhost:5000/health
curl http://localhost:5000/environment
```

The `/environment` endpoint should return `production`, confirming the variable is being read correctly and is not hardcoded.

---

## Jenkins Pipeline Setup

1. Open Jenkins at `http://localhost:8080`
2. Create a new Pipeline job
3. Under Pipeline, select **Pipeline script from SCM**
4. Set SCM to Git, paste the repository URL
5. Set branch to `develop`
6. Set Script Path to `Jenkinsfile`
7. Save and click Build Now

The pipeline runs six stages: Checkout, Install, Test, Build, Tag, and Health Check. A test failure stops the pipeline at the Test stage and the remaining stages do not run.

---

## Merge Conflict

A controlled conflict was created between two feature branches that both modified the `APP_VERSION` variable in `app.py`. One branch set it to `1.1.0` and the other to `2.0.0`. When both were merged into `develop`, Git flagged the conflict. The resolution was to keep `1.1.0` as the agreed version, remove the conflict markers, and commit the resolved file with a message explaining what was changed and why.

---

## Windows-Specific Issues Faced

**pytest could not find app.py during test collection**

When running `pytest tests/ -v` from the project root, Python could not resolve `from app import app` in the test file. This does not happen on Linux because the current directory is usually in the Python path by default. On Windows it is not. The fix was adding a `pytest.ini` file with `pythonpath = .` which tells pytest to include the project root when resolving imports. Without this file committed to the repository, Jenkins also fails for the same reason.

**Jenkins pipeline used `sh` instead of `bat`**

The Jenkinsfile was written using `sh` commands which is the Linux shell executor. Jenkins on Windows does not have `sh` available and throws a `CreateProcess error=2` immediately. Every `sh` step had to be replaced with `bat`, and environment variable references inside batch commands had to change from `${VAR}` to `%VAR%` syntax.

**`timeout` command fails in Jenkins batch steps**

The `timeout /t 5 /nobreak` command works in an interactive Windows terminal but not inside Jenkins batch steps because Jenkins runs them without an interactive session. The error is `Input redirection is not supported`. The workaround was replacing it with `ping -n 6 127.0.0.1 > nul` which achieves the same five second wait without requiring any user input.

---

## AI Assistance

Claude was used during this project for debugging specific errors — primarily the Windows pytest path issue, the sh/bat Jenkins compatibility problem, and the timeout command failure. All code was tested, understood, and verified manually before submission.
