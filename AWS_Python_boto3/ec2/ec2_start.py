import boto3
import sys
from botocore.exceptions import ClientError

instance_id = ""

ec2 = boto3.client('ec2')

try:
    ec2.start_instances(InstanceIds = [instance_id], DryRun=True)
    print()
except ClientError as e:
    if 'DryRunOperation' not in str(e):
        raise

try:
    response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
    print(response)
except ClientError as e:
    print(e)