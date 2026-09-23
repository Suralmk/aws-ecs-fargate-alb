# 02 — Containerized FastAPI on ECS Fargate + ALB

> **Difficulty:** Starter
> **Category:** Core Compute — the backbone of modern AWS deployments

Containerize a FastAPI application with Docker, push the image to Elastic Container Registry, and deploy it on ECS Fargate behind an Application Load Balancer with auto-scaling. This project replaces manual EC2 management with a fully managed container runtime — and teaches you the operational model that most AWS production workloads use today.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                        Internet                         │
└────────────────────────┬────────────────────────────────┘
                         │
              ┌──────────▼──────────┐
              │  Application Load   │
              │  Balancer (ALB)     │  ← HTTPS via ACM
              └──────┬──────────────┘
                     │  Target Group
          ┌──────────┴──────────┐
          │                     │
   ┌──────▼──────┐       ┌──────▼──────┐
   │ Fargate Task│       │ Fargate Task│   ← Auto Scaled
   │  (AZ-1)     │       │  (AZ-2)     │
   └──────┬──────┘       └──────┬──────┘
          │                     │
          └──────────┬──────────┘
                     │
         ┌───────────▼───────────┐
         │   ECS Cluster         │
         │   (no EC2 to manage)  │
         └───────────────────────┘
                     │
         ┌───────────▼───────────┐
         │   ECR Private Registry│  ← Docker image pushed here
         └───────────────────────┘
```

- Docker image built locally and pushed to **ECR**
- ECS Cluster runs **Fargate tasks** (no EC2 to manage)
- **ALB** distributes traffic across tasks in multiple AZs
- **Application Auto Scaling** adds/removes tasks based on CPU utilization
- **Secrets Manager** injects database credentials at container startup

---

## AWS Services Used

| Category | Services |
|---|---|
| **Container** | ECR, ECS Cluster, Task Definitions, Fargate |
| **Networking** | Application Load Balancer, Target Groups |
| **Scaling** | Application Auto Scaling |
| **Security** | Secrets Manager, IAM Task Roles, ACM (SSL) |
| **Observability** | CloudWatch Logs, CloudWatch Container Insights |
| **DNS** | Route 53 (custom domain) |
| **Config** | Parameter Store |

---

## Tech Stack

### Backend / API
- **FastAPI** (Dockerized)
- **Gunicorn + Uvicorn** workers
- **SQLAlchemy + Alembic** (ORM & migrations)
- **Pydantic Settings** (environment config)
- Health check endpoint at `/health`

### DevOps / IaC
- **Dockerfile** (multi-stage: build + runtime)
- **Docker Compose** (local development)
- **Terraform** ECS module
- **AWS CDK** (`EcsPattern`)
- **GitHub Actions** CI/CD pipeline
- **buildspec.yml** (AWS CodeBuild)

---

## What You Will Build

- [ ] Multi-stage Dockerfile for FastAPI (build + runtime stages)
- [ ] ECR repository with image lifecycle policies
- [ ] ECS task definition with CPU, memory, env vars, and secrets
- [ ] ALB with HTTPS listener and ACM certificate
- [ ] Auto-scaling policy (target tracking on CPU 70%)
- [ ] Rolling deployment with health check validation

---

## Key Skills Demonstrated

- Task definitions vs ECS services
- IAM task roles vs execution roles
- ALB health check tuning
- Rolling vs blue/green ECS deployments
- CloudWatch Container Insights setup
- Cost comparison: Fargate vs EC2 launch type

---

## Getting Started

### Prerequisites
- AWS CLI configured (`aws configure`)
- Docker installed and running
- Terraform or AWS CDK installed

### Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start the API
uvicorn app.main:app --reload
```

### Build & Push Docker Image to ECR

```bash
# Authenticate Docker to ECR
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com

# Build the image
docker build -t aws-container-lab .

# Tag and push
docker tag aws-container-lab:latest <account-id>.dkr.ecr.<region>.amazonaws.com/aws-container-lab:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/aws-container-lab:latest
```

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Root — service info |
| `GET` | `/health` | Health check (used by ALB) |
| `GET` | `/info` | Hostname, environment, version |
| `GET` | `/metrics` | Uptime in seconds |

---

## Project Structure

```
aws-ecs-fargate-alb/
├── app/
│   └── main.py              # FastAPI application
├── Dockerfile               # Multi-stage Docker build
├── docker-compose.yml       # Local development
├── requirements.txt         # Python dependencies
└── README.md
```

---

## Cost Comparison

| Launch Type | Management | Pricing Model |
|---|---|---|
| **Fargate** | Fully managed (no EC2) | Per vCPU/memory per second |
| **EC2** | You manage instances | Per EC2 instance hour |

> Fargate is ideal for variable workloads. EC2 launch type is more cost-effective at high, sustained utilization.

---

## License

MIT
