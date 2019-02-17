#! /usr/bash/python

import boto3
import botocore

s3 = boto3.resource('s3')

try:
    data = open('/Users/abhinav.korpal/Documents/githiub/Python/images/aws_python_boto.png', 'rb')
    s3.Bucket('my-bucket').put_object(Key='aws_python_boto.png', Body=data)
    print("The object Upload")
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        pass