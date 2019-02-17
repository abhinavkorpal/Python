import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')

try:
    response = ec2.delete_security_group(GroupId='sg-006490a47d62dd659')
    print('Security Group Deleted')
except ClientError as e:
    print(e)

