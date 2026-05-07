# Project-CloudWatch-Logs-copied-to-S3-via-EventBridge-scheduled-Lambda-Invocation
CloudWatch Logs are copied to S3 via EventBridge scheduled Lambda Invocation


Environment Variables for Lambda

| Key               | Value                                           |
| ----------------- | ----------------------------------------------- |
| `LOG_GROUP_NAMES` | `ec2-all-logs,ec2-httpd-access,ec2-httpd-error` |
| `S3_BUCKET_NAME`  | `your-s3-bucket-name`                           |
| `S3_PREFIX`       | `Cloudwatch-EC2-Logs/`                          |
| `EXPORT_HOURS`    | `24`                                            |
