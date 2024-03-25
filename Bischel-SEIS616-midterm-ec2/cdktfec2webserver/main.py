#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, Token, Fn

from imports.aws.instance import Instance
from imports.aws.vpc import Vpc
from imports.aws.iam_role import IamRole
from imports.aws.s3_bucket import S3Bucket
from imports.aws.s3_object import S3Object

import os



class MyStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # define resources here
        
        
        InstanceRole = IamRole(self, "InstanceSSM",
                        assume_role_policy=Token.as_string(
                            Fn.jsonencode({
                                "Statement": [{
                                    "Action": "sts:AssumeRole",
                                    "Effect": "Allow",
                                    "Principal": {
                                        "Service": "ec2.amazonaws.com"
                                    },
                                    "Sid": ""
                            }
                            ],
                            "Version": "2012-10-17"
                            })),
                    name="test_role",
                    tags={
                        "tag-key": "tag-value"
                     }           
                    )
        
        
        
        cdktf_web_instance = Instance(self, "cdktf_web_instance",
                                        ami = "ami-0c101f26f147fa7fd",
                                        instance_type = "t3.small")

        script_s3_bucket = S3Bucket(self, "script_s3_bucket")
        
        script_s3_object = S3Object(self, "script_s3_object", 
                            bucket = "script_s3_bucket",
                            etag=Token.as_string(Fn.filemd5("/cdktfec2webserver/")),
                            key = "server_script.sh"
                            )
                            
        









app = App()
MyStack(app, "cdktfec2webserver")

app.synth()
