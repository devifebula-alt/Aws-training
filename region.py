import boto3


test = boto3.client('s3')
region = boto3.session.Session().region_name

print(region)