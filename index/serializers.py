from rest_framework import serializers

from .models import DeploymentInfo, Instance


class DeploymentInfoSerializer(serializers.ModelSerializer):

    instance = serializers.PrimaryKeyRelatedField(
        many=False, queryset=Instance.objects.all())

    class Meta:
        model = DeploymentInfo
        fields = ('instance', 'date', 'commit_hash')
