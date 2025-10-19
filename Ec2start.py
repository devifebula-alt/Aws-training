import boto3

def stop():
    IAM = boto3.client('iam')
    client=boto3.client('ec2',region_name='us-west-1')
    response = client.stop_instances(
        InstanceIds=[
            'i-0c1feb08b52005d9f',
        ],
    )

    print(response)

def start():
    IAM = boto3.client('iam')
    client=boto3.client('ec2',region_name='us-west-1')
    response = client.start_instances(
        InstanceIds=[
            'i-0c1feb08b52005d9f',
        ],
    )

    print(response)
if __name__ == "__main__":
    print('going to stop instances')      
    print('') 
    stop()
