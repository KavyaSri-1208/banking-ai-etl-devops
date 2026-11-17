output "api_ecr_repository_url" {
  value = aws_ecr_repository.api.repository_url
}
output "frontend_ecr_repository_url" {
  value = aws_ecr_repository.frontend.repository_url
}
output "etl_ecr_repository_url" {
  value = aws_ecr_repository.etl.repository_url
}
output "data_bucket_name" {
  value = aws_s3_bucket.data.bucket
}
