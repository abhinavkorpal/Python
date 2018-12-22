### Create an AWS VPC

This Python script creates a two availability zone VPC in the AWS region of choice. It will create 4 equal
size Subnets; two public and two private.

**Requirements:**

* Tested with:
   * Python version: 3.7.0
   * Boto3 version: 1.7.50
   * Botocore version: 1.10.50
   * Netaddr version: 0.7.19
* Valid AWS API keys/profile

**Setup:**

Update with your AWS profile / credentials.  Modify the region, VPC CIDR and VPC name (used for tagging)
parameters.

```
main(profile = '<YOUR_PROFILE>', region = 'us-west-2', cidr = '10.64.0.0/22', name = 'test-dev')
```

**Usage:**

```
python create_vpc.py
```

**Output:**

```
vpc_id: vpc-08230e0e712a493c8
igw_id: igw-069b014026e4a7414
sub_id: subnet-0210b79e9c87fec37 size: 10.64.0.0/24 zone: us-west-2a tier: public
sub_id: subnet-011144cc1a9da4897 size: 10.64.1.0/24 zone: us-west-2b tier: public
sub_id: subnet-0a94ee29e4b941811 size: 10.64.2.0/24 zone: us-west-2a tier: private
sub_id: subnet-02d17efe37c56f029 size: 10.64.3.0/24 zone: us-west-2b tier: private
rtb_id: rtb-0b2ea67bca5d9e919 tier: public
rtb_id: rtb-0b584bd58ed1b92d5 tier: private
acl_id: acl-035062164b0c971dd tier: public
acl_id: acl-0d5437aa2994b7997 tier: private
flw_id: fl-0fe7e9d190d9bbb01
```

**To Do:**

- [x] Enable VPC flow logs
- [ ] NAT gateways

**References:**

* https://netaddr.readthedocs.io/en/latest/
* https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
* https://blogs.aws.amazon.com/security/post/Tx3NVS2JAL7KWOM/How-to-Help-Prepare-for-DDoS-Attacks-by-Reducing-Your-Attack-Surface

