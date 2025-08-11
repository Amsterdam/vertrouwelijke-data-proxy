from django.conf import settings
from django.http import FileResponse
from rest_framework.generics import RetrieveAPIView
from rest_framework.request import Request

from vertrouwelijke_data_proxy.files import permissions
from vertrouwelijke_data_proxy.files.clients import ConfidentialDataClient


class ProxyConfidentialDataView(RetrieveAPIView):

    needed_scopes: set = None
    client: ConfidentialDataClient

    permission_classes = []

    def initial(self, request: Request, *args, **kwargs):
        """DRF-level initialization for all request types."""

        # Perform authorization, permission checks and throttles.
        super().initial(request, *args, **kwargs)

        self.user_scopes = set(request.get_token_scopes)

    def get_client(self) -> ConfidentialDataClient:
        """Provide the AzureSearchServiceClient. This can be overwritten per view if needed."""
        return ConfidentialDataClient(
            base_url=settings.AZURE_STORAGE_CONTAINER_ENDPOINT,
            client_id=settings.MANAGED_IDENTITY_CLIENT_ID,
        )

    def get(self, request: Request, *args, **kwargs):
        self.client = self.get_client()

        stream = self.client.call(request=request)
        return FileResponse(stream, as_attachment=True)

    def get_permissions(self):
        """Collect the DRF permission checks.
        DRF checks these in the initial() method, and will block view access
        if these permissions are not satisfied.
        """

        return super().get_permissions() + [
            permissions.IsFpMdw(),
        ]
