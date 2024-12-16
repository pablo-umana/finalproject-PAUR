from diagrams import Diagram, Cluster
from diagrams.aws.compute import ECS, ElasticContainerService
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB, CloudFront, Route53
from diagrams.aws.storage import S3
from diagrams.aws.devtools import Codebuild, Codepipeline
from diagrams.aws.management import Cloudformation

with Diagram("Arquitectura AWS - Sistema de Generación de PDFs", show=False, direction="LR"):

    # DNS y CDN
    dns = Route53("Route 53")
    cdn = CloudFront("CloudFront")

    with Cluster("Frontend"):
        s3 = S3("Static Website")

    # Pipeline de CI/CD
    with Cluster("CI/CD Pipeline"):
        pipeline = Codepipeline("CodePipeline")
        build = Codebuild("CodeBuild")

    # Servicios de Backend
    with Cluster("Backend Services"):
        lb = ELB("Load Balancer")
        with Cluster("ECS Cluster"):
            services = [
                ECS("API Service 1"),
                ECS("API Service 2"),
                ECS("API Service 3")
            ]

    # Base de Datos
    with Cluster("Database"):
        db = RDS("PostgreSQL")

    # Infraestructura como Código
    cfn = Cloudformation("CloudFormation")

    # Conexiones
    dns >> cdn >> s3
    dns >> lb >> services
    pipeline >> build
    build >> s3
    build >> services

    for service in services:
        service >> db

    cfn - [s3, lb, db]  # CloudFormation gestiona estos recursos