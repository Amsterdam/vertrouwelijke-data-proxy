from django.urls import reverse
from vertrouwelijke_data_proxy.files.views import ProxyConfidentialDataView


class TestProxyConfidentialDataView:
    """Prove that the generic view offers the login check logic.
    This is tested through the concrete implementations though.
    """

    def test_unauthorized_403(self, api_client):
        """No scope == no access"""
        url = reverse("confidential-data-index")
        response = api_client.get(url)
        assert response.status_code == 403

    def test_authorized_400_on_index(self, api_request_fp_mdw):
        """Not requesting file shows 400"""
        url = reverse("confidential-data-index")
        request = api_request_fp_mdw(url)
        response = ProxyConfidentialDataView().get(request)
        assert response.status_code == 400

    def test_authorized_404_on_non_existent_file(
        self, patch_azure_blob_doesnt_exist, api_request_fp_mdw
    ):
        """Not requesting file shows 400"""
        url = reverse("confidential-data-index")
        request = api_request_fp_mdw(url + "non-file.zip")
        response = ProxyConfidentialDataView().get(request)
        assert response.status_code == 404

    def test_file_download(self, patch_vdclient, api_request_fp_mdw):
        url = reverse("confidential-data-index")
        request = api_request_fp_mdw(url + "file.zip")
        response = ProxyConfidentialDataView().get(request)
        assert response.status_code == 200
        assert response.filename == "file.zip"
        assert response.file_to_stream.read() == b"0000"
