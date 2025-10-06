from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Объекттин ээсине гана жазуу уруксаты
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Колдонуучу объект же колдонуучунун өзү болушу керек
        return obj == request.user or obj.id == request.user.id


class IsAdminUser(permissions.BasePermission):
    """
    Персонал же администраторлор үчүн гана уруксат
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsSuperUser(permissions.BasePermission):
    """
    Суперколдонуучулар үчүн гана уруксат
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser