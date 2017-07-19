#!/bin/python

import boto.ec2


conn = boto.ec2.connect_to_region("us-west-2")
conn.stop_instances(instance_ids=['instance-id-1','instance-id-2'])
