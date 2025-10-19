import boto3
from collections import defaultdict
from openpyxl import Workbook
import csv

# Initialize clients
iam = boto3.client('iam')
s3 = boto3.client('s3')
account_id = boto3.client('sts').get_caller_identity()['Account']
region = boto3.session.Session().region_name

# Collect data for Excel sheets
iam_data = defaultdict(list)
s3_data = defaultdict(list)

# Also collect unified data for CSV
csv_data = []

# === IAM USERS ===
iam_users = iam.list_users()['Users']
for user in iam_users:
    username = user['UserName']
    user_arn = user['Arn']
    tags = iam.list_user_tags(UserName=username)['Tags']
    department = next((tag['Value'] for tag in tags if tag['Key'] == 'Department'), 'Unknown')
    
    iam_data[department].append(username)
    csv_data.append({
        'ResourceType': 'IAM User',
        'ResourceName': username,
        'Department': department,
        'ResourceARN': user_arn
    })

# === S3 BUCKETS ===
buckets = s3.list_buckets()['Buckets']
for bucket in buckets:
    bucket_name = bucket['Name']
    try:
        tags = s3.get_bucket_tagging(Bucket=bucket_name)['TagSet']
        department = next((tag['Value'] for tag in tags if tag['Key'] == 'Department'), 'Unknown')
    except Exception:
        department = 'Untagged'

    bucket_arn = f"arn:aws:s3:::{bucket_name}"
    s3_data[department].append(bucket_name)
    csv_data.append({
        'ResourceType': 'S3 Bucket',
        'ResourceName': bucket_name,
        'Department': department,
        'ResourceARN': bucket_arn
    })

# === EXCEL EXPORT ===
wb = Workbook()

# Sheet 1: IAM Users
ws1 = wb.active
ws1.title = "IAM Users"
ws1.append(["Department", "UserName"])
for dept, users in iam_data.items():
    for user in users:
        ws1.append([dept, user])

# Sheet 2: S3 Buckets
ws2 = wb.create_sheet("S3 Buckets")
ws2.append(["Department", "BucketName"])
for dept, buckets in s3_data.items():
    for bucket in buckets:
        ws2.append([dept, bucket])

# Save Excel file
excel_file = "aws_audit_report.xlsx"
wb.save(excel_file)
print(f"✅ Excel report saved to {excel_file}")

# === CSV EXPORT ===
csv_file = "aws_audit_report.csv"
with open(csv_file, mode='w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["ResourceType", "ResourceName", "Department", "ResourceARN"])
    writer.writeheader()
    writer.writerows(csv_data)

print(f"✅ CSV report saved to {csv_file}")
