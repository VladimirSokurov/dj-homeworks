from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Advertisement
from .serializers import AdvertisementSerializer
from .filters import AdvertisementFilter
from .permissions import AccessPermission


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    # queryset = Advertisement.objects.all()
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            permissions = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            permissions = [AccessPermission]
        else:
            permissions = []
        return [permission() for permission in permissions]

    def destroy(self, request, *args, **kwargs):
        user = request.user
        posts = Advertisement.objects.filter(creator=user, status='OPEN').count()
        if posts >= 10:
            return super(AdvertisementViewSet, self).destroy(request, *args, **kwargs)
