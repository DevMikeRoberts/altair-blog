# Usage

## Local Development

Start the development server:

```bash
cd altair-blog/app
source .venv/bin/activate
python manage.py runserver
```

Visit `http://localhost:8000` to view the blog.

## Running Tests

```bash
cd altair-blog/app
python manage.py test
```

Tests run against an in-memory SQLite database — no external DB required.

## Deployment

Deployment is fully automated via GitHub Actions.

1. Push to `main` triggers the deploy workflow
2. Terraform provisions/updates AWS infrastructure
3. Docker image is built and pushed to ECR
4. ECS service is force-deployed with the new image

The ALB URL is output at the end of the deploy workflow.

## Infrastructure Management

Terraform state is managed remotely. To plan or apply changes manually:

```bash
cd altair-blog/infra
terraform init
terraform plan
terraform apply
```

## Environment Variables

The app requires these environment variables in production:

| Variable       | Description            |
|----------------|------------------------|
| `DB_NAME`      | PostgreSQL database     |
| `DB_USER`      | Database user           |
| `DB_PASSWORD`  | Database password       |
| `DB_HOST`      | RDS endpoint            |
| `DB_PORT`      | Database port (5432)    |
| `SECRET_KEY`   | Django secret key       |
| `DJANGO_DEBUG` | Debug mode (false in production) |
