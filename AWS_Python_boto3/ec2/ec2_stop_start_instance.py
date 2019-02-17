import boto3
from botocore.exceptions import ClientError

ec2 = boto3.resource('ec2')

ids = ['instance-id-1', 'instance-id-2']

def stop():
    ec2.instances.filter(InstanceIds=ids).stop()

def start():
    ec2.instances.filter(InstanceIds=ids).terminate()

