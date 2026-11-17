variable "aws_region" {
  description = "AWS region for the demo resources"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Name prefix for resources"
  type        = string
  default     = "banking-ai-etl"
}

variable "bucket_name" {
  description = "Globally unique S3 bucket name for project data"
  type        = string
}

variable "enable_versioning" {
  type    = bool
  default = true
}
