import boto3
import os
from datetime import datetime, timedelta
import time

logs_client = boto3.client('logs')

# Environment Variables
LOG_GROUP_NAMES = os.environ['LOG_GROUP_NAMES'].split(',')

S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']

S3_PREFIX = os.environ.get(
    'S3_PREFIX',
    'Cloudwatch-EC2-Logs/'
)

EXPORT_HOURS = int(
    os.environ.get('EXPORT_HOURS', '24')
)


def lambda_handler(event, context):

    now = datetime.utcnow()

    from_time = now - timedelta(hours=EXPORT_HOURS)

    # Convert to milliseconds
    from_timestamp = int(from_time.timestamp() * 1000)
    to_timestamp = int(now.timestamp() * 1000)

    export_results = []

    for log_group in LOG_GROUP_NAMES:

        log_group = log_group.strip()

        task_name = (
            f"{log_group}-"
            f"{now.strftime('%Y%m%d-%H%M%S')}"
        )

        try:
            response = logs_client.create_export_task(
                taskName=task_name,
                logGroupName=log_group,
                fromTime=from_timestamp,
                to=to_timestamp,
                destination=S3_BUCKET_NAME,
                destinationPrefix=f"{S3_PREFIX}{log_group}"
            )

            export_results.append({
                'logGroup': log_group,
                'taskId': response['taskId'],
                'status': 'SUCCESS'
            })

            # CloudWatch export task limit protection
            time.sleep(5)

        except Exception as e:

            export_results.append({
                'logGroup': log_group,
                'status': 'FAILED',
                'error': str(e)
            })

    return {
        'statusCode': 200,
        'results': export_results
    }