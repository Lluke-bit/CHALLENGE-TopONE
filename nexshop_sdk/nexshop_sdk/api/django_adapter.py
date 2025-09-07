# nexshop_sdk/api/django_adapter.py

from django.http import JsonResponse
from django.urls import path


# View para verificar a saúde do serviço
def healthcheck(request):
    """
    Endpoint de verificação de saúde.
    """
    return JsonResponse({"status": "ok", "framework": "Django"})


# URLConf para o aplicativo Django
urlpatterns = [
    path("healthcheck/", healthcheck, name="healthcheck"),
]
