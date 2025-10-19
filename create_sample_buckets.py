import boto3
import uuid
import random
import time

s3 = boto3.client('s3')
region = 'us-west-1'

departments = ["Engineering", "Finance", "HR", "Marketing", "Sales"]

# Create 6 S3 buckets with department tags
for i in range(6):
    dept = random.choice(departments)
    bucket_name = f"devops-{dept.lower()}-{uuid.uuid4().hex[:6]}"
    try:
        print(f"Creating bucket: {bucket_name} ({dept})")
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
        s3.put_bucket_tagging(
            Bucket=bucket_name,
            Tagging={'TagSet': [{"Key": "Department", "Value": dept}]}
        )
        time.sleep(0.5)  # avoid throttling
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"Bucket {bucket_name} already exists.")
