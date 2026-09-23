# aws-ecs-fargate-alb

A containerized FastAPI application deployed on AWS ECS Fargate behind an Application Load Balancer with auto-scaling.

## Architecture

Docker images are stored in ECR and run as Fargate tasks across multiple availability zones. An ALB routes HTTPS traffic to the tasks, with Application Auto Scaling adjusting capacity based on CPU utilization. Secrets Manager handles database credentials at container startup.

```
Internet → ALB (HTTPS/ACM) → Target Group → Fargate Tasks (multi-AZ)
                                                      ↑
                                              ECR (Docker image)
```

## Stack

- **FastAPI** with Gunicorn + Uvicorn workers
- **SQLAlchemy + Alembic** for database and migrations
- **Pydantic Settings** for environment configuration
- **ECS Fargate** — no EC2 instances to manage
- **Terraform / AWS CDK** for infrastructure
- **GitHub Actions** for CI/CD

## AWS Services

- ECR — private container registry
- ECS Cluster + Task Definitions (Fargate)
- Application Load Balancer + Target Groups
- Application Auto Scaling (CPU target tracking at 70%)
- Secrets Manager + Parameter Store
- ACM (SSL) + Route 53
- CloudWatch Container Insights + Logs
- IAM Task Roles & Execution Roles

## Getting Started

```bash
# Run locally
pip install -r requirements.txt
uvicorn app.main:app --reload
```

```bash
# Build and push to ECR
aws ecr get-login-password --region <region> | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com

docker build -t aws-container-lab .
docker tag aws-container-lab:latest <account-id>.dkr.ecr.<region>.amazonaws.com/aws-container-lab:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/aws-container-lab:latest
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Service info |
| `GET` | `/health` | ALB health check |
| `GET` | `/info` | Hostname and environment |
| `GET` | `/metrics` | Uptime |

## Project Structure

```
├── app/
│   └── main.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## License

MIT
