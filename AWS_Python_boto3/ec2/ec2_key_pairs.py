import boto3

ec2 = boto3.client('ec2')
response = ec2.describe_key_pairs()
print(response)

def create_key_pair():
    response = ec2.create_key_pair(KeyName='KEY_PAIR_NAME')
    print(response)

def delete_key_pair():
    response = ec2.delete_key_pair(KeyName='KEY_PAIR_NAME')
    print(response)