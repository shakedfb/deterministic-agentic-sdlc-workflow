terraform {
  required_version = ">= 1.7"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "agentic-sdlc-tf-state"
    key    = "platform/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  default = "us-east-1"
}

variable "environment" {
  default = "production"
}

variable "project" {
  default = "agentic-sdlc"
}

# --- ECS Cluster for Temporal Workers ---

resource "aws_ecs_cluster" "workers" {
  name = "${var.project}-workers-${var.environment}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Project     = var.project
    Environment = var.environment
  }
}

# --- ElastiCache Redis ---

resource "aws_elasticache_cluster" "state" {
  cluster_id           = "${var.project}-state"
  engine               = "redis"
  node_type            = "cache.t4g.medium"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379

  tags = {
    Project     = var.project
    Environment = var.environment
  }
}

# --- RDS PostgreSQL for Temporal + LangGraph Checkpoints ---

resource "aws_db_instance" "temporal" {
  identifier     = "${var.project}-temporal-db"
  engine         = "postgres"
  engine_version = "16"
  instance_class = "db.t4g.medium"
  allocated_storage    = 50
  max_allocated_storage = 200

  db_name  = "temporal"
  username = "temporal"
  password = "CHANGE_ME_IN_SECRETS_MANAGER"

  skip_final_snapshot = false
  final_snapshot_identifier = "${var.project}-temporal-final"
  backup_retention_period   = 7

  tags = {
    Project     = var.project
    Environment = var.environment
  }
}

# --- ECR Repository for Worker Images ---

resource "aws_ecr_repository" "worker" {
  name                 = "${var.project}/worker"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Project     = var.project
    Environment = var.environment
  }
}

output "ecs_cluster_arn" {
  value = aws_ecs_cluster.workers.arn
}

output "redis_endpoint" {
  value = aws_elasticache_cluster.state.cache_nodes[0].address
}

output "rds_endpoint" {
  value = aws_db_instance.temporal.endpoint
}
