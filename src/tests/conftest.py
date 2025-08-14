from __future__ import annotations

import io
from pathlib import Path

import pytest
from azure.storage.blob import BlobClient
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.test import APIClient, APIRequestFactory
from vertrouwelijke_data_proxy.files.clients import ConfidentialDataClient

HERE = Path(__file__).parent


@pytest.fixture()
def api_request_fp_mdw() -> WSGIRequest:

    def make_request(path):
        request = APIRequestFactory().get(path)
        request.get_token_scopes = ["FP/MDW"]
        return request

    return make_request


@pytest.fixture()
def patch_vdclient(monkeypatch):
    def get_stream(*args, **kwargs):
        return io.BytesIO(b"0000")

    monkeypatch.setattr(ConfidentialDataClient, "call", get_stream)


@pytest.fixture()
def patch_azure_blob_doesnt_exist(monkeypatch):
    def nope(_self):
        return False

    monkeypatch.setattr(BlobClient, "exists", nope)


@pytest.fixture()
def api_client() -> APIClient:
    """Return a client that has unhindered access to the API views"""
    api_client = APIClient()
    api_client.default_format = "json"  # instead of multipart
    return api_client
