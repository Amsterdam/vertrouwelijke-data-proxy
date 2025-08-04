from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r"^.*",
        views.ProxyConfidentialDataView.as_view(),
        name="confidential-data-index",
    )
]
