
from imports.aws.s3_bucket_website_configuration import S3BucketWebsiteConfiguration
#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, TerraformAsset, AssetType, Token


from imports.aws.provider import AwsProvider
from imports.aws.s3_bucket import S3Bucket
# from imports.aws.ec2_host import Ec2Host
from imports.aws.vpc import Vpc
from imports.aws.instance import Instance
from imports.aws.s3_bucket_object import S3BucketObject
from imports.aws.vpc_ipv4_cidr_block_association import VpcIpv4CidrBlockAssociation
from imports.aws.launch_template import LaunchTemplate
from imports.aws.s3_bucket_website_configuration import S3BucketWebsiteConfiguration
from imports.aws.data_aws_s3_object import DataAwsS3Object

import os


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # define resources here
        AwsProvider(self, "AWS", region="us-east-1")
        
        website_bucket = S3Bucket(self, "website_bucket",
                 bucket="midtermwebserver",
                 tags={"Name": "Test"
                 }
                 )
        
        

        S3BucketWebsiteConfiguration(self, "example",
            bucket=Token.as_string(website_bucket.id),
                error_document=S3BucketWebsiteConfigurationErrorDocument(
                key="error.html"
                ),
                index_document=S3BucketWebsiteConfigurationIndexDocument(
                suffix="index.html"
                ),
                routing_rule=[S3BucketWebsiteConfigurationRoutingRule(
                condition=S3BucketWebsiteConfigurationRoutingRuleCondition(
                    key_prefix_equals="docs/"
                ),
                redirect=S3BucketWebsiteConfigurationRoutingRuleRedirect(
                    replace_key_prefix_with="documents/"
                )
            )
            ]
        )