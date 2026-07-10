# ALB — internet-facing
resource "aws_security_group" "alb" {
  name        = "altair-alb"
  description = "HTTP/HTTPS from internet"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTP from internet"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "HTTPS from internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    description = "All outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = { Name = "altair-alb-sg" }
}

# ECS — traffic from ALB only
resource "aws_security_group" "ecs" {
  name        = "altair-ecs"
  description = "Traffic from ALB to ECS"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "HTTP from ALB"
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }
  egress {
    description = "All outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = { Name = "altair-ecs-sg" }
}

# RDS — PostgreSQL from ECS only
resource "aws_security_group" "rds" {
  name        = "altair-rds"
  description = "PostgreSQL from ECS"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "PostgreSQL from ECS"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs.id]
  }
  tags = { Name = "altair-rds-sg" }
}

resource "aws_default_security_group" "default" {
  vpc_id = aws_vpc.main.id

  tags = { Name = "altair-default-sg" }
}
