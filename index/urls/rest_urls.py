from django.conf.urls import url, include
from rest_framework import routers

from index.viewsets import DeploymentInfoViewSet

router = routers.DefaultRouter()
router.register(r'deploymentinfos', DeploymentInfoViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
