from rest_framework import viewsets

from index.models import DeploymentInfo
from index.serializers import DeploymentInfoSerializer


class DeploymentInfoViewSet(viewsets.ModelViewSet):

    queryset = DeploymentInfo.objects.all()
    serializer_class = DeploymentInfoSerializer
