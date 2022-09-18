from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from Endpoint.api import serializers
from Data import models


class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )

    serializer_class = serializers.UsersSerializer
    queryset = models.Users.objects.all()