"""

Enable VPC flow logs.

Python Version: 3.7.0
Boto3 Version: 1.7.50

"""

import boto3
from botocore.exceptions import ClientError

import json


class Templates():

  TrustPolicy = {
                  'Version': '2012-10-17',
                  'Statement': [
                    {
                      'Sid': '',
                      'Effect': 'Allow',
                      'Principal': {
                        'Service': 'vpc-flow-logs.amazonaws.com'
                      },
                      'Action': 'sts:AssumeRole'
                    }
                  ]
                }

  LogsPolicy =  {
                  'Version': '2012-10-17',
                  'Statement': [
                    {
                      'Action': [
                        'logs:CreateLogGroup',
                        'logs:CreateLogStream',
                        'logs:DescribeLogGroups',
                        'logs:DescribeLogStreams',
                        'logs:PutLogEvents'
                      ],
                      'Effect': 'Allow',
                      'Resource': '*'
                    }
                  ]
                }


class Flow():

  def __init__(self, profile, region, vpc_id):

    # AWS Credentials
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

    self.session = boto3.Session(profile_name=profile)

    self.ec2  = self.session.client('ec2',  region_name=region)
    self.iam  = self.session.client('iam',  region_name=region)
    self.logs = self.session.client('logs', region_name=region)

    # Naming convention

    self.role_name   = 'flowlogsRole'
    self.policy_name = 'flowlogsPolicy'
    self.logs_name   = 'flowlogsGroup' + '-' + vpc_id


  def create_iam_role(self):
    """
    Create flow logs IAM role and policy
    """

    # Create VPC flows logs IAM role

    role_exists = False

    args = {
      'Path' : '/',
      'RoleName' : self.role_name,
      'AssumeRolePolicyDocument' : json.dumps(Templates.TrustPolicy)
    }

    try:
      role = self.iam.create_role(**args)
    except ClientError as e:
      if e.response['Error']['Code'] == 'EntityAlreadyExists':

        try:
          role = self.iam.get_role(RoleName = self.role_name)
        except ClientError as e:
          print(e.response['Error']['Message'])
          return None

        role_exists = True

      else:
        print(e.response['Error']['Message'])
        return None

    role_arn  = role['Role']['Arn']

    if role_exists == True:
      return role_arn


    # Create VPC flow logs IAM policy

    args = {
      'Path' : '/',
      'PolicyName' : self.policy_name,
      'Description' : 'Grant access to CloudWatch Logs.',
      'PolicyDocument' : json.dumps(Templates.LogsPolicy)
    }

    try:
      policy = self.iam.create_policy(**args)
    except ClientError as e:
      print(e.response['Error']['Message'])
      return None

    policy_arn = policy['Policy']['Arn']

    # Attach policy to the IAM role

    try:
      result = self.iam.attach_role_policy(
        RoleName = self.role_name,
        PolicyArn = policy_arn
      )
    except ClientError as e:
      print(e.response['Error']['Message'])
      return None

    return role_arn


  def create_logs_group(self):
    """
    Create CloudWatch Logs group
    """

    # Create CloudWatch Logs group

    try:
      group = self.logs.create_log_group(logGroupName = self.logs_name)
    except ClientError as e:
      print(e.response['Error']['Message'])
      return None

    # Set logs retention period
    # Possible values are: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1827, and 3653.

    try:
      result = self.logs.put_retention_policy(
        logGroupName = self.logs_name,
        retentionInDays = 30
      )
    except ClientError as e:
      print(e.response['Error']['Message'])

    return self.logs_name


  def create_flow(self, vpc_id, logs_name, role_arn):
    """
    Create VPC flow logs
    """

    # Enable VPC flow logs

    args = {
      'ResourceIds' : [ vpc_id ],
      'ResourceType' : 'VPC',
      'TrafficType' : 'ALL',
      'LogGroupName' : logs_name,
      'DeliverLogsPermissionArn' : role_arn
    }

    try:
      flow_ids = self.ec2.create_flow_logs(**args)
    except ClientError as e:
      print(e.response['Error']['Message'])
      return None

    flow_id = flow_ids['FlowLogIds'][0]

    return flow_id


def main(profile, region, vpc_id):
  """
  Do the work..
  """

  flow = Flow(profile, region, vpc_id)

  role_arn = flow.create_iam_role()

  if role_arn != None:
    print('Using IAM role: {}'.format(flow.role_name))

    logs_name = flow.create_logs_group()

    if logs_name != None:
      print('Using CloudWatch Logs group: {}'.format(logs_name))

      flow_id = flow.create_flow(vpc_id, logs_name, role_arn)

      if flow_id != None:
        print('Created VPC flow logs: {}'.format(flow_id))

  return


if __name__ == "__main__":

  main(profile = 'abcdef', region = 'us-east-1', vpc_id = 'vpc-******')

