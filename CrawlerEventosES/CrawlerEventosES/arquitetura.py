from diagrams import Cluster, Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import SQS
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.database import RDS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.general import User, Client

with Diagram("Arquitetura WebCrawler EventosES", show=False): 
    user = User("Actor")
    
    api_gateway = APIGateway("API Gateway")
    user >> api_gateway

    with Cluster("Crawler Services"):
        lebillet_crawler = Lambda("Lebillet Crawler")
        agazeta_crawler = Lambda("Agazeta Crawler")
        
        api_gateway >> lebillet_crawler
        api_gateway >> agazeta_crawler

    event_queue = SQS("Fila de Evento")
    lebillet_crawler >> event_queue
    agazeta_crawler >> event_queue

    
    with Cluster("Processamento"):
        data_processor = Lambda("Processador de Dados")
        raw_storage = S3("Armazenamento Dados Brutos")
        
        event_queue >> data_processor
        data_processor >> raw_storage

    database = RDS("Banco de Dados")
    data_processor >> database

    with Cluster("Monitoramento e Notificações"):
        monitor = Cloudwatch("Monitoramento")
        notification_service = Client("Serviço de Notificações")

    data_processor >> monitor
    monitor >> notification_service
