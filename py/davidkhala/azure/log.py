import os
from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient

endpoint = os.environ['DATA_COLLECTION_ENDPOINT']
credential = DefaultAzureCredential()
logs_client = LogsIngestionClient(endpoint, credential)