from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    CfnOutput,
    CfnTag,
)

from constructs import Construct


class CdkEc2Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(
            self,
            "MyVpc",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public-subnet-1",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                )
            ],
        )

        # Create Security Group
        sec_group = ec2.SecurityGroup(
            self, "MySecurityGroup", vpc=vpc, allow_all_outbound=True
        )

        # Create Security Group Ingress Rule
        sec_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "allow SSH access"
        )

        # Create Key Pair
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_ec2/CfnKeyPair.html
        cfn_key_pair = ec2.CfnKeyPair(
            self,
            "MyCfnKeyPair",
            key_name="cdk-ec2-key-pair",
            public_key_material="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC/2jrt/59NIHGWL4hGnymp0svgRYDXeigqMjf55klXLgVFx9A+OFggdvKz+4tVW0vWgL1C50cjBfAN/nBQZDq8V67qETWj3Azf4ULF9eaQ5ax9/r3fBZa935z3sgZLkRUnCbqQ+OSgGHLOb01u0X1lgbPNwue5Sc0LSs4JDd1aFTr8wX2Ea5rDktF0k2g4Gs3KMGWAN8hWx95Et9CoOWllvS2m00wPj0qm9gbkqLcPWE+bOoZYAXlww163k/qPEiPh+BgxMQXxplOuZ1FX5YsLsjbJqSll4m6XbysVnGYq/wAGPxxWQdPoXsUiIA0m6/K4iaF4wN1/Xz4408rlr8fb9nfqGBksWz5cUYIl/bUXzDzJF22ZLHKOSUS8OQ0NLDLBkISyFtc27VK8whDK7P/ZKYrixvHSQt0+sKUeJa+aVU0hC3G3oR4OpoZn8PLr9hqUccUTolzBWngwEQwDjBXUvvLTfiXYlEzlAhM1fEbOXsJcaAVez3pFVMy3t7bbjbU= ryzon@ryzon711",
            tags=[CfnTag(key="key", value="value")],
        )

        # Create EC2 instance
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_ec2/README.html
        # https://docs.aws.amazon.com/linux/al2023/ug/what-is-amazon-linux.html
        instance = ec2.Instance(
            self,
            "MyInstance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            vpc=vpc,
            security_group=sec_group,
            associate_public_ip_address=True,
            key_name=cfn_key_pair.key_name,
        )
        # Output Instance ID
        CfnOutput(self, "InstanceId", value=instance.instance_id)
