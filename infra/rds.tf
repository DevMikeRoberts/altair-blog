resource "aws_db_subnet_group" "main" {
  name       = "altair-main"
  subnet_ids = aws_subnet.data[*].id
  tags       = { Name = "altair-rds-subnet-group" }
}

resource "random_password" "db" {
  length  = 24
  special = false
}

resource "aws_secretsmanager_secret" "db" {
  name = "altair-blog-db"
}

resource "aws_secretsmanager_secret_version" "db" {
  secret_id = aws_secretsmanager_secret.db.id
  secret_string = jsonencode({
    host     = aws_db_instance.main.address
    port     = aws_db_instance.main.port
    db_name  = aws_db_instance.main.db_name
    username = aws_db_instance.main.username
    password = aws_db_instance.main.password
  })
}

resource "random_id" "snapshot" {
  byte_length = 4
}

resource "aws_db_instance" "main" {
  identifier = "altair-blog"

  engine         = "postgres"
  engine_version = "16.3"
  instance_class = var.db_instance_class

  allocated_storage     = 20
  max_allocated_storage = 0
  storage_type          = "gp3"
  storage_encrypted     = true

  db_name  = "altairblog"
  username = "altair"
  password = random_password.db.result

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  backup_retention_period = 1
  backup_window           = "03:00-04:00"
  maintenance_window      = "sun:04:00-sun:05:00"

  enabled_cloudwatch_logs_exports = ["postgresql"]

  skip_final_snapshot       = false
  final_snapshot_identifier = "altair-blog-final-${random_id.snapshot.hex}"
  deletion_protection       = true

  auto_minor_version_upgrade = true
  copy_tags_to_snapshot      = true

  tags = { Name = "altair-blog" }
}
