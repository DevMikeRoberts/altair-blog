# Development

## Prerequisites

- Python 3.12
- Docker (optional, for containerized development)
- AWS account (for full infrastructure deployment)

## Local Setup

```bash
cd altair-blog/app

# Create and activate virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python manage.py test

# Start development server
python manage.py runserver
```

The test suite uses an in-memory SQLite database (see `app/test_settings.py`) and fast password hashing, so tests run quickly without external dependencies.

## Project Structure

```
altair-blog/
├── .github/workflows/   # CI/CD pipeline definitions
├── app/                  # Django application
│   ├── blog/            # Main Django project config
│   ├── posts/           # Blog posts app
│   ├── Dockerfile       # Production container image
│   ├── entrypoint.sh    # Container entrypoint (migrate + gunicorn)
│   └── requirements.txt # Python dependencies
├── infra/               # Terraform infrastructure
│   ├── main.tf          # Provider and backend config
│   ├── vpc.tf           # Networking
│   ├── ecs.tf           # ECS cluster and service
│   ├── ecr.tf           # Container registry
│   ├── rds.tf           # PostgreSQL database
│   ├── alb.tf           # Load balancer
│   ├── iam.tf           # IAM roles and policies
│   └── security-groups.tf
└── docs/                # Documentation
```

## Code Conventions

- Python: follow PEP 8
- Django: use class-based views and REST Framework serializers
- Terraform: use `terraform fmt` before committing
- CI checks run on every PR — make sure tests and IaC checks pass

## Making Changes

1. Create a feature branch from `main`
2. Make changes, keeping tests passing
3. Open a pull request
4. CI runs checks automatically
5. Merge to `main` triggers deployment
