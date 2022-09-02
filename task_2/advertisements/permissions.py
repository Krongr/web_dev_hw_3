from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User


class OwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.creator:
            return True
        _user = User.objects.get(username=request.user)
        return _user.is_superuser

class Draft(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.status == "DRAFT":
            return request.user == obj.creator
        return True