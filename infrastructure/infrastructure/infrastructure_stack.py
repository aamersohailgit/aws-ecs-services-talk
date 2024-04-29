from aws_cdk import (
    Stack,
    aws_ec2 as ec2
)
from constructs import Construct
from aws_cdk import aws_ecs as ecs


class InfrastructureStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        
