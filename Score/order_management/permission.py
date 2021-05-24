__all__ = [
    'PermissionCashier',
    'PermissionAccountant',
]

from django.contrib.auth.models import Permission, Group
from django.contrib.auth.models import User


class PermissionCashier:

    def has_permission(self, request, view):
        return bool(
            request.user.has_perm('order_management.add_order') and request.user.has_perm(
                'order_management.change_order') and request.user.has_perm('order_management.view_product'),
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.has_perm('order_management.add_order') and request.user.has_perm(
                'order_management.change_order') and request.user.has_perm('order_management.view_product'),
        )


class PermissionAccountant:

    def has_permission(self, request, view):
        return bool(
            request.user.has_perm('order_management.view_order'),
        )

