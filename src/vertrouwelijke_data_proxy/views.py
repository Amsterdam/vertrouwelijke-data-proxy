from django.http import JsonResponse
from django.views import View


class RootView(View):
    """Root page of the server."""

    def get(self, request, *args, **kwargs):
        return JsonResponse({"status": "online"})
