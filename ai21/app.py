#!/usr/bin/env python3
import aws_cdk as cdk
from os import environ
from json import loads
from constructs import Construct
from aws_cdk import (
  aws_ec2 as ec2,
  aws_secretsmanager as sm,
  aws_iam as iam,
  aws_kendra as kendra,
  aws_lambda as lambda_,
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

class KnowledgeStoreConstruct(Construct):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    role = iam.Role(self, 'KendraRole',
      assumed_by=iam.ServicePrincipal('kendra.amazonaws.com'),
      managed_policies=[
        iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchLogsFullAccess'),
        iam.ManagedPolicy.from_aws_managed_policy_name('AmazonKendraFullAccess'),
      ])

    insurance_index = kendra.CfnIndex(self,'InsuranceIndex',
      edition='DEVELOPER_EDITION',
      role_arn= role.role_arn,
      name='InsuranceIndex')
    
    insurance_ds = kendra.CfnDataSource(self,'InsuranceDataSource',
      index_id=insurance_index.ref,
      name='InsuranceDataSource',
      type='WEBCRAWLER',
      role_arn= role.role_arn,
      data_source_configuration= kendra.CfnDataSource.DataSourceConfigurationProperty(
        web_crawler_configuration=kendra.CfnDataSource.WebCrawlerConfigurationProperty(
          crawl_depth=10,
          max_links_per_page=1000,
          max_urls_per_minute_crawl_rate=60,
          max_content_size_per_page_in_mega_bytes=50,
          urls= kendra.CfnDataSource.WebCrawlerUrlsProperty(
              site_maps_configuration=kendra.CfnDataSource.WebCrawlerSiteMapsConfigurationProperty(
                site_maps=['https://www.newyorklife.com/sitemapindex.xml',                           
                           'https://www.newyorklife.com/sitemap-agents.xml']))
          )))
    
    financial_knowledge = kendra.CfnDataSource(self,'GeneralFinancialDataSource',
      index_id=insurance_index.ref,
      name='GeneralFinancialDataSource',
      type='WEBCRAWLER',
      role_arn= role.role_arn,
      data_source_configuration= kendra.CfnDataSource.DataSourceConfigurationProperty(
        web_crawler_configuration=kendra.CfnDataSource.WebCrawlerConfigurationProperty(
          urls= kendra.CfnDataSource.WebCrawlerUrlsProperty(
              site_maps_configuration=kendra.CfnDataSource.WebCrawlerSiteMapsConfigurationProperty(
                site_maps=[
                  'https://www.investopedia.com/sitemap_1.xml',
                  'https://www.investopedia.com/sitemap_2.xml',
                  #'https://www.investopedia.com/google-news-sitemap.xml'
                ]))
          )))
    
    kendra.CfnDataSource(self,'BalanceMoney',
      index_id=insurance_index.ref,
      name='BalanceMoneyDataSource',
      type='WEBCRAWLER',
      role_arn= role.role_arn,
      data_source_configuration= kendra.CfnDataSource.DataSourceConfigurationProperty(
        web_crawler_configuration=kendra.CfnDataSource.WebCrawlerConfigurationProperty(
          urls= kendra.CfnDataSource.WebCrawlerUrlsProperty(
              site_maps_configuration=kendra.CfnDataSource.WebCrawlerSiteMapsConfigurationProperty(
                site_maps=[
                  'https://www.thebalancemoney.com/sitemap.xml',
                ]
          )))))
          
class WebInterfaceConstruct(Construct):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    with(open('api_key.json','rt')) as f:
      secret = sm.Secret(self,'Secret',
        description='AI21 API Key',
        secret_name='AI21_APIKey',
        secret_string_value=cdk.SecretValue.unsafe_plain_text(f.read()))
      
    self.role = iam.Role(self, 'LambdaRole',
      assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
      managed_policies=[
        iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchLogsFullAccess'),
        iam.ManagedPolicy.from_aws_managed_policy_name('AmazonKendraFullAccess'),
      ])

    secret.grant_read(self.role)

class GenAIDemoStack(cdk.Stack):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    self.networking = NetworkingConstruct(self, 'NetworkingConstruct')
    self.knowledge_store = KnowledgeStoreConstruct(self, 'KnowledgeStoreConstruct')
    self.web_ux = WebInterfaceConstruct(self,'WebInterface')

class GenAIDemoApp(cdk.App):  
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.gen_ai_demo = GenAIDemoStack(self, 'GenAIDemoStack')


environ['CDK_DEFAULT_ACCOUNT'] = '995765563608'
environ['CDK_DEFAULT_REGION'] = 'us-east-1'


app = GenAIDemoApp()
app.synth()    