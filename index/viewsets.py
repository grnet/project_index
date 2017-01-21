from rest_framework import viewsets

from .models import DeploymentInfo
from .serializers import DeploymentInfoSerializer


class DeploymentInfoViewSet(viewsets.ModelViewSet):

    queryset = DeploymentInfo.objects.all()
    serializer_class = DeploymentInfoSerializer
    
