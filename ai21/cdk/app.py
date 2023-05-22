#!/usr/bin/env python3
import aws_cdk as cdk
from os import environ
from constructs import Construct
from aws_cdk import (
  aws_ec2 as ec2,
  aws_lambda_event_sources as events,
  aws_ses as sqs,
  aws_iam as iam,
)

class NetworkingConstruct(Construct):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    self.vpc = ec2.Vpc(self, 'VPC',
      max_azs=3,
      nat_gateways=1,
      subnet_configuration=[
        ec2.SubnetConfiguration(name='Public', subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24),
        ec2.SubnetConfiguration(name='Default', subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS, cidr_mask=18)
      ])

class GenAIDemoStack(cdk.Stack):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    self.networking = NetworkingConstruct(self, 'NetworkingConstruct')

class GenAIDemoApp(cdk.App):  
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.gen_ai_demo = GenAIDemoStack(self, 'GenAIDemoStack')


environ['CDK_DEFAULT_ACCOUNT'] = '995765563608'
environ['CDK_DEFAULT_REGION'] = 'us-east-1'


app = GenAIDemoApp()
app.synth()    