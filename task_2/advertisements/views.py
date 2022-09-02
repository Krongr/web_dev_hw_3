from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.contrib.auth.models import User

from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from advertisements.permissions import Draft, OwnerOrAdmin
from advertisements.filters import AdvertisementFilter


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    def get_queryset(self):
        _user_id = self.request.user.id
        return Advertisement.objects.exclude(
            ~Q(creator=_user_id) & Q(status='DRAFT')
        )
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["retrieve",]:
            return [Draft()]
        if self.action in ["create",]:
            return [IsAuthenticated()]
        if self.action in ["update", "partial_update", "destroy",]:
            return [OwnerOrAdmin()]
        return []
