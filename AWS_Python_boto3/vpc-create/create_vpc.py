"""

Create an AWS VPC.

Python Version: 3.7.0
Boto3 Version: 1.7.50

"""

import boto3
from botocore.exceptions import ClientError
from enable_flows import Flow

# https://netaddr.readthedocs.io/en/latest/
from netaddr import *

# pip install netaddr


class Tag():

  def __init__(self, name, resource):

    self.name = name.lower() + '-' + resource

  def resource(self, ec2, resource_id):

    try:
      result = ec2.create_tags(
        Resources = [
          resource_id 
        ],
        Tags = [
          {
            'Key': 'Name',
            'Value': self.name
          }
        ]
      )
    except ClientError as e:
      print(e.response['Error']['Message'])


def create_vpc(ec2, cidr, name):
  """
  Create a VPC
  """

  # Create the VPC

  args = {
    'CidrBlock' : cidr,
    'InstanceTenancy' : 'default'
  }

  try:
    vpc = ec2.create_vpc(**args)['Vpc']
  except ClientError as e:
    print(e.response['Error']['Message'])
    return None

  vpc_id = vpc['VpcId']

  # Add DNS support
  # modify_vpc_attribute() only updates one attribute at a time

  try:
    result = ec2.modify_vpc_attribute(
      EnableDnsSupport = {
          'Value': True
      },
      VpcId = vpc_id
    )

    result = ec2.modify_vpc_attribute(
      EnableDnsHostnames = {
        'Value': True
      },
      VpcId = vpc_id
    )
  except ClientError as e:
    print(e.response['Error']['Message'])

  # Tag the resource

  tag = Tag(name, 'vpc'); tag.resource(ec2, vpc_id)
  print('vpc_id: {}'.format(vpc_id))

  return vpc_id


def create_igw(ec2, vpc_id, name):
  """
  Create and attach an internet gateway
  """

  # Create the gateway

  try:
    igw = ec2.create_internet_gateway()['InternetGateway']
  except ClientError as e:
    print(e.response['Error']['Message'])
    return None

  igw_id = igw['InternetGatewayId']

  # Attach the gateway

  try:
    result = ec2.attach_internet_gateway(
      InternetGatewayId = igw_id,
      VpcId = vpc_id
    )
  except ClientError as e:
    print(e.response['Error']['Message'])

  # Tag the resource

  tag = Tag(name, 'igw'); tag.resource(ec2, igw_id)
  print('igw_id: {}'.format(igw_id))

  return igw_id


def subnet_sizes(cidr):
  """
  Calculate subnets sizes
  """

  # Permitted netmasks

  netmasks = (
    '255.255.255.0',
    '255.255.254.0',
    '255.255.252.0',
    '255.255.248.0',
    '255.255.240.0',
    '255.255.224.0',
    '255.255.192.0',
    '255.255.128.0',
    '255.255.0.0'
  )

  ip = IPNetwork(cidr)
  mask = ip.netmask

  if str(mask) not in netmasks:
    print('Netmask not allowed: {}'.format(mask))
    return None

  # Create 4 equal size subnet blocks with the available CIDR space

  for n, netmask in enumerate(netmasks):
    if str(mask) == netmask:
      subnets = list(ip.subnet(26 - n))

  return subnets


def create_sub(ec2, vpc_id, subnets, zones, name):
  """
  Create subnets
  """

  i = 0
  subnet_ids = []
  tier = 'public'

  for subnet in subnets:

    # Create a subnet

    args = {
      'AvailabilityZone' : zones[i],
      'CidrBlock' : str(subnet),
      'VpcId' : vpc_id
    }

    try:
      sub = ec2.create_subnet(**args)['Subnet']
    except ClientError as e:
      print(e.response['Error']['Message'])
      return None

    subnet_id = sub['SubnetId']
    subnet_ids.append(subnet_id)

    # Tag the resource

    tag = Tag(name, 'sub' + '-' + tier); tag.resource(ec2, subnet_id)
    print('sub_id: {} size: {} zone: {} tier: {}'.format(subnet_id, subnet, zones[i], tier))

    i += 1

    if i == 2:
      i = 0
      tier = 'private'

  return subnet_ids


def create_rtb(ec2, vpc_id, subnet_ids, igw_id, name):
  """
  Create and associate route tables
  """

  i = 0
  route_table_ids = []
  tier = 'public'

  for subnet in subnet_ids:
    if i == 0:

      # Create a route table

      try:
        rtb = ec2.create_route_table(VpcId=vpc_id)['RouteTable']
      except ClientError as e:
        print(e.response['Error']['Message'])
        return

      rtb_id = rtb['RouteTableId']
      route_table_ids.append(rtb_id)

      # Add a default route to the public route table

      if tier == 'public' and igw_id != None:
        try:
          result = ec2.create_route(
            DestinationCidrBlock = '0.0.0.0/0',
            GatewayId = igw_id,
            RouteTableId = rtb_id
          )
        except ClientError as e:
          print(e.response['Error']['Message'])

      # Tag the resource

      tag = Tag(name, 'rtb' + '-' + tier); tag.resource(ec2, rtb_id)
      print('rtb_id: {} tier: {}'.format(rtb_id, tier))

    # Associate each subnet with a route table

    try:
      result = ec2.associate_route_table(
        RouteTableId = rtb_id,
        SubnetId = subnet
      )
    except ClientError as e:
      print(e.response['Error']['Message'])

    i += 1

    if i == 2:
      i = 0
      tier = 'private'

  return route_table_ids


def create_acl(ec2, vpc_id, subnet_ids, cidr, name):
  """
  Create and associate network access lists 
  """

  i = 0
  acl_ids = []
  tier = 'public'

  # Grab the default acl subnet associations

  args = {
    'Filters' : [
      {
        'Name' : 'vpc-id',
        'Values' : [ vpc_id ]
      }
    ]
  }

  try:
    default_acl = ec2.describe_network_acls(**args)['NetworkAcls']
  except ClientError as e:
    print(e.response['Error']['Message'])
    default_acl_associations = []

  else:
    default_acl_associations = default_acl[0]['Associations']

  for subnet in subnet_ids:
    if i == 0:

      # Create a network access list

      try:
        acl = ec2.create_network_acl(VpcId=vpc_id)['NetworkAcl']
      except ClientError as e:
        print(e.response['Error']['Message'])
        return

      acl_id = acl['NetworkAclId']
      acl_ids.append(acl_id) 

      # Create ingress rules

      try:
        result = ec2.create_network_acl_entry(
          CidrBlock = '0.0.0.0/0',
          Egress = False,
          NetworkAclId = acl_id,
          PortRange = {
            'From': 443,
            'To': 443
          },
          Protocol = '6',
          RuleAction = 'allow',
          RuleNumber = 100
        )
        result = ec2.create_network_acl_entry(
          CidrBlock = '0.0.0.0/0',
          Egress = False,
          NetworkAclId = acl_id,
          PortRange = {
            'From': 80,
            'To': 80
          },
          Protocol = '6',
          RuleAction = 'allow',
          RuleNumber = 200
        )
        result = ec2.create_network_acl_entry(
          CidrBlock = '0.0.0.0/0',
          Egress = False,
          NetworkAclId = acl_id,
          PortRange = {
            'From': 1024,
            'To': 65535
          },
          Protocol = '6',
          RuleAction = 'allow',
          RuleNumber = 300
        )
        result = ec2.create_network_acl_entry(
          CidrBlock = cidr,
          Egress = False,
          NetworkAclId = acl_id,
          PortRange = {
            'From': 22,
            'To': 22
          },
          Protocol = '6',
          RuleAction = 'allow',
          RuleNumber = 400
        )
      except ClientError as e:
        print(e.response['Error']['Message'])

      # Create egress rules

      try:
        result = ec2.create_network_acl_entry(
          CidrBlock = '0.0.0.0/0',
          Egress = True,
          NetworkAclId = acl_id,
          PortRange = {
            'From': 443,
            'To': 443
          },
          Protocol = '6',
          RuleAction = 'allow',
          RuleNumber = 100
        )
        result = ec2.create_network_acl_entry(
          CidrBlock = '0.0.0.0/0',
          Egress = True,
          NetworkAclId = acl_id,
          PortRange = {
            'From': 80,
            'To': 80
          },
          Protocol = '6',
          RuleAction = 'allow',
          RuleNumber = 200
        )
        result = ec2.create_network_acl_entry(
          CidrBlock = '0.0.0.0/0',
          Egress = True,
          NetworkAclId = acl_id,
          PortRange = {
            'From': 1024,
            'To': 65535
          },
          Protocol = '6',
          RuleAction = 'allow',
          RuleNumber = 300
        )
        result = ec2.create_network_acl_entry(
          CidrBlock = cidr,
          Egress = True,
          NetworkAclId = acl_id,
          PortRange = {
            'From': 22,
            'To': 22
          },
          Protocol = '6',
          RuleAction = 'allow',
          RuleNumber = 400
        )
      except ClientError as e:
        print(e.response['Error']['Message'])

      # Tag the resource

      tag = Tag(name, 'acl' + '-' + tier); tag.resource(ec2, acl_id)
      print('acl_id: {} tier: {}'.format(acl_id, tier))

    # Associate each subnet with a network access list

    if len(default_acl_associations) > 0:
      association_id = None
      for association in default_acl_associations:
        if association['SubnetId'] == subnet:
          association_id = association['NetworkAclAssociationId']

      if association_id != None:
        try:
          result = ec2.replace_network_acl_association(
            AssociationId = association_id,
            NetworkAclId = acl_id
        )
        except ClientError as e:
          print(e.response['Error']['Message'])

    i += 1

    if i == 2:
      i = 0
      tier = 'private'

  return acl_ids


def get_zones(ec2):
  """
  Return all available zones in the region
  """

  zones = []

  try:
    aws_zones = ec2.describe_availability_zones()['AvailabilityZones']
  except ClientError as e:
    print(e.response['Error']['Message'])
    return None

  for zone in aws_zones:
    if zone['State'] == 'available':
      zones.append(zone['ZoneName'])

  return zones


def create_flow(profile, region, vpc_id):
  """
  Enable VPC flow logs
  """

  flow = Flow(profile, region, vpc_id)

  # Create IAM role and policy

  role_arn = flow.create_iam_role()

  # Create CloudWatch Logs group

  if role_arn != None:
    logs_name = flow.create_logs_group()

  # Enable VPC flow logs

    if logs_name != None:
      flow_id = flow.create_flow(vpc_id, logs_name, role_arn)

      if flow_id != None:
        print('flw_id: {}'.format(flow_id))

  return


def main(profile, region, cidr, name):
  """
  Do the work..

  Order of operation:

  1.) Create the VPC
  2.) Create and attach an internet gateway
  3.) Calculate subnet sizes (netaddr)
  4.) Create the subnets
  5.) Create and associate route tables
  6.) Create and associate network access lists
  7.) Enable VPC flow logs
  """

  # AWS Credentials
  # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

  session = boto3.Session(profile_name=profile)
  ec2 = session.client('ec2', region_name=region)

  # Grab the available zones

  zones = get_zones(ec2)
  if zones == None or len(zones) < 2:
    return

  # Calculate the subnet sizes

  subnets = subnet_sizes(cidr)
  if subnets == None:
    return

  vpc_id  = create_vpc(ec2, cidr, name)
  if vpc_id == None:
    return

  igw_id  = create_igw(ec2, vpc_id, name)
  sub_ids = create_sub(ec2, vpc_id, subnets, zones, name)
  if sub_ids == None:
    return

  rtb_ids = create_rtb(ec2, vpc_id, sub_ids, igw_id, name)
  acl_ids = create_acl(ec2, vpc_id, sub_ids, cidr, name)
  flow_id = create_flow(profile, region, vpc_id)

  return


if __name__ == "__main__":

  main(profile = 'abcde', region = 'us-east-1', cidr = '10.64.0.0/22', name = 'test-dev')

