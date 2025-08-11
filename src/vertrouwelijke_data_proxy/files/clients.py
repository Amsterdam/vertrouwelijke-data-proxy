import io
import logging

from azure.identity import ManagedIdentityCredential
from azure.storage.blob import BlobServiceClient
from rest_framework.request import Request

logger = logging.getLogger(__name__)

USER_AGENT = "Amsterdam-Vertrouwelijke-Data-Proxy/1.0"


class ConfidentialDataClient:
    def __init__(self, base_url, client_id) -> None:
        """Initialize the client configuration.

        :param base_url: Base URL of the Search Backend
        """
        azure_credential = ManagedIdentityCredential(client_id=client_id)
        self.blob_service_client = BlobServiceClient(
            account_url=base_url, credential=azure_credential
        )

    def call(self, request: Request) -> io.BytesIO:
        stream = io.BytesIO()
        blob_client = self.blob_service_client.get_blob_client("bulk-data-fp-mdw", request.path)
        blob_client.download_blob().read_into(stream)

        return stream
