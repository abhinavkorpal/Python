import boto3
from botocore.exceptions import ClientError

ec2 = boto3.resource('ec2')

try:
    instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        print(instance.id, instance.instance_type)
except ClientError as e:
    print(e)