from aws_cdk import aws_ecs as ecs, aws_iam as iam, aws_logs as logs
from constructs import Construct
from aws_cdk import Stack
from dotenv import dotenv_values


class TaskDefinitionStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Load environment variables from .env.task_definition_config
        env_config = dotenv_values(".env.task_definition_config")

        # Define the ECS Task Definition for users-api
        users_api_task_def = self.create_fargate_task_definition(
            task_family=env_config["TASK_FAMILY"],
            task_role_arn=env_config["TASK_ROLE_ARN"],
            execution_role_arn=env_config["EXECUTION_ROLE_ARN"],
            container_name="users-api",
            image_uri=env_config["IMAGE_URI"],
            container_port=int(env_config["CONTAINER_PORT"]),
            cpu=int(env_config["CPU"]),  # Convert CPU to integer
            memory=int(env_config["MEMORY"]),  # Convert Memory to integer
            log_group_name=env_config["LOG_GROUP_NAME"],
            log_stream_prefix=env_config["LOG_STREAM_PREFIX"],
        )

    def create_fargate_task_definition(
        self,
        task_family,
        task_role_arn,
        execution_role_arn,
        container_name,
        image_uri,
        container_port,
        cpu,
        memory,
        log_group_name,
        log_stream_prefix,
    ):

        # Create ECS Task Role and Execution Role from ARNs
        task_role = iam.Role.from_role_arn(self, "TaskRole", role_arn=task_role_arn)
        execution_role = iam.Role.from_role_arn(
            self, "ExecRole", role_arn=execution_role_arn
        )

        # Define the ECS Task Definition
        task_definition = ecs.FargateTaskDefinition(
            self,
            f"{task_family}TaskDef",
            family=task_family,
            cpu=cpu,
            memory_limit_mib=int(memory),
            task_role=task_role,
            execution_role=execution_role,
        )

        # Add the container definition to the task
        container = task_definition.add_container(
            f"{container_name}",
            image=ecs.ContainerImage.from_registry(image_uri),
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix=log_stream_prefix,
                log_group=logs.LogGroup.from_log_group_name(
                    self, f"{container_name}_LogGroup", log_group_name
                ),
            ),
        )

        # Add port mappings to the container
        container.add_port_mappings(
            ecs.PortMapping(container_port=container_port, protocol=ecs.Protocol.TCP)
        )

        return task_definition
