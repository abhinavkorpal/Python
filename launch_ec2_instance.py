#!/bin/python

import boto.ec2

conn = boto.ec2.connect_region("us-west-2")
conn.run_instance(
     'ami-6sdef556',
     key_name='xxxxxxxxxxxxx'
     instance_type='t1.micro'
     security_group=['xxxxxxxxxx']
)
