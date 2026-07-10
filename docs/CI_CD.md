# CI/CD

## Workflows

### CI (`ci.yml`)

Triggers on pull requests to `main`. Runs three jobs in parallel:

- **Checkov** — IaC security scanning on `infra/` Terraform files
- **Terraform Checks** — `terraform fmt -check` and `terraform validate`
- **Django Tests** — Python 3.12, installs deps from `app/requirements.txt`, runs `python manage.py test` with `DJANGO_SETTINGS_MODULE=test_settings`

### Deploy (`deploy.yml`)

Triggers on pushes to `main`. Runs sequentially:

1. **validate** — Same security and lint checks as CI
2. **deploy** — Configures AWS credentials, logs into ECR, runs `terraform apply` on `infra/`, builds and pushes Docker image to ECR, forces new ECS deployment, and outputs the ALB DNS name

## Infrastructure Deployment

Terraform manages all AWS resources:

- VPC with public/private subnets
- ECS Fargate cluster and service
- ECR repository for Docker images
- RDS PostgreSQL instance
- Application Load Balancer
- Security groups and IAM roles

See `infra/` for Terraform configurations.
