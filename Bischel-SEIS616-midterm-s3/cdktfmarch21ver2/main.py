#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, TerraformAsset, AssetType, Token


from imports.aws.provider import AwsProvider

# from imports.aws.ec2_host import Ec2Host
from imports.aws.vpc import Vpc
from imports.aws.instance import Instance
from imports.aws.s3_bucket import S3Bucket
from imports.aws.s3_bucket_object import S3BucketObject
from imports.aws.launch_template import LaunchTemplate
from imports.aws.s3_bucket_website_configuration import S3BucketWebsiteConfiguration
from imports.aws.data_aws_s3_object import DataAwsS3Object

import os


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # define resources here
        AwsProvider(self, "AWS", region="us-east-1")

        # bucket = S3Bucket(self, "bucket",
        #          bucket="midtermwebserver",
        #          tags={"Name": "Test"
        #          }
        #          )
         
        # webserver_vpc = Vpc(self, "server_vpc",
        #                 cidr_block="10.0.0.0/16"
        #                 )   
                        
        servervpc = Vpc(self, "servervpc",
               cidr_block="10.0.0.0/16",
               )   
        
        
        server_script = DataAwsS3Object(self, "server_script",
            bucket="webserver-deploy-config",
            key="/cdktfmarch21ver2/wsscript.sh"
        )
        webserver = Instance(self, "webserver",
                    ami="ami-0c101f26f147fa7fd",
                    instance_type="t2.micro",
                    user_data=Token.as_string(server_script.body)
        )




        
        # LaunchTemplate(self, "snow",
        #               placement=LaunchTemplatePlacement(
        #               availability_zone="us-east-1"
        #               ), 
        
        
        # Instance(self, "compute", 
        #         ami = "ami-0c101f26f147fa7fd",
        #         instance_type = "t3.small"
        #         #name = "midtermserver",
        #         #user_data="wsscript.sh"
        #         )   
        
     

app = App()
stack = MyStack(app, "bucket")

app.synth()