from aws_cdk import aws_ecs as ecs, aws_iam as iam, aws_logs as logs
from constructs import Construct
from aws_cdk import Stack
from dotenv import dotenv_values


class EcsClusterStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Load environment variables from .env.ecs_cluster_config
        env_config = dotenv_values("config/.env.ecs_cluster_config")

        # create ECS cluster
        ecs_cluster = ecs.CfnCluster(
            self,
            env_config.get("CLUSTER_NAME"),
            capacity_providers=["FARGATE_SPOT", "FARGATE"],
            cluster_name=env_config.get("CLUSTER_NAME"),
            cluster_settings=[
                ecs.CfnCluster.ClusterSettingsProperty(
                    name="containerInsights", value="enabled"
                ),
            ],
        )
