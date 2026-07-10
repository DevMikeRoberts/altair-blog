resource "aws_ecs_cluster" "main" {
  name = "altair-blog"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  tags = { Name = "altair-blog" }
}

resource "aws_ecs_cluster_capacity_providers" "main" {
  cluster_name       = aws_ecs_cluster.main.name
  capacity_providers = ["FARGATE", "FARGATE_SPOT"]

  default_capacity_provider_strategy {
    capacity_provider = "FARGATE"
    weight            = 1
  }
}

resource "aws_cloudwatch_log_group" "app" {
  name              = "/ecs/altair-blog"
  retention_in_days = 365
  tags              = { Name = "altair-blog" }
}

resource "aws_ecs_task_definition" "app" {
  family                   = "altair-blog"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([
    {
      name      = "app"
      image     = "${aws_ecr_repository.app.repository_url}:latest"
      essential = true
      portMappings = [
        { containerPort = 8000, protocol = "tcp" }
      ]
      environment = [
        { name = "DJANGO_SETTINGS_MODULE", value = "blog.settings" },
        { name = "ALLOWED_HOSTS", value = "*" },
        { name = "DJANGO_DEBUG", value = "False" },
      ]
      secrets = [
        { name = "DB_HOST", valueFrom = "${aws_secretsmanager_secret.db.arn}:host::" },
        { name = "DB_PORT", valueFrom = "${aws_secretsmanager_secret.db.arn}:port::" },
        { name = "DB_NAME", valueFrom = "${aws_secretsmanager_secret.db.arn}:db_name::" },
        { name = "DB_USER", valueFrom = "${aws_secretsmanager_secret.db.arn}:username::" },
        { name = "DB_PASSWORD", valueFrom = "${aws_secretsmanager_secret.db.arn}:password::" },
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.app.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])
  tags = { Name = "altair-blog" }
}

resource "aws_ecs_service" "app" {
  name                   = "altair-blog"
  cluster                = aws_ecs_cluster.main.id
  task_definition        = aws_ecs_task_definition.app.arn
  desired_count          = 1
  launch_type            = "FARGATE"
  enable_execute_command = true

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  network_configuration {
    subnets          = aws_subnet.private[*].id
    security_groups  = [aws_security_group.ecs.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "app"
    container_port   = 8000
  }

  depends_on = [aws_lb_listener.http]
  tags       = { Name = "altair-blog" }
}
