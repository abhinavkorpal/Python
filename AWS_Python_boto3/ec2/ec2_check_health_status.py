import boto3
import json
from botocore.exceptions import ClientError
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

ec2 = boto3.resource('ec2')

try:
    for status in ec2.meta.client.describe_instance_status()['InstanceStatuses']:
        #print(json.dumps(status, sort_keys=True, indent=4))
        print(highlight(json.dumps(status, sort_keys=True, indent=4), JsonLexer(), TerminalFormatter()))
except ClientError as e:
    print(e)