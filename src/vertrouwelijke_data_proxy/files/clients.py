import io
import logging

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from rest_framework.request import Request

logger = logging.getLogger(__name__)

USER_AGENT = "Amsterdam-Vertrouwelijke-Data-Proxy/1.0"


class ConfidentialDataClient:
    def __init__(self, base_url) -> None:
        """Initialize the client configuration.

        :param base_url: Base URL of the Search Backend
        """
        azure_credential = DefaultAzureCredential()
        self.blob_service_client = BlobServiceClient(
            account_url=base_url, credential=azure_credential
        )

    def call(self, request: Request) -> io.BytesIO:
        stream = io.BytesIO()
        blob_path = request.path[1:]  # path always starts with a '/'
        if blob_path.startswith("bulk-data-fp-mdw"):  # this matches the ingress.yaml
            blob_path = blob_path.split("/", 1)[1]  # just keep the part after 'bulk-data-fp-mdw/'
        blob_client = self.blob_service_client.get_blob_client("bulk-data-fp-mdw", blob_path)
        blob_client.download_blob().readinto(stream)

        return stream
