from diagrams import Cluster, Diagram
from diagrams.onprem import client, compute, database, inmemory
from diagrams.programming import framework, language

with Diagram("Kibune Overview", show=False):
    http_client = client.Client("HTTP client")
    api = framework.FastAPI("REST API (FastAPI)")
    db = database.MySQL("Database (MySQL)")
    redis = inmemory.Redis("Job queue (Redis)")
    receiver = compute.Server("Receiver")

    with Cluster("Job queue"):
        worker_group = [
            language.Python("Worker 1"),
            language.Python("Worker 2"),
            language.Python("Worker 3"),
        ]

    http_client >> api
    api >> db
    api >> redis >> worker_group

    worker_group >> db
    worker_group >> receiver
