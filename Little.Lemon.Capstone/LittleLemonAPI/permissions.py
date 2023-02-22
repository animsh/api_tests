from rest_framework import permissions


class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_superuser


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.groups.filter(name='Manager').exists()


class IsDeliveryCrew(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.groups.filter(name='Delivery Crew').exists()

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.groups.filter(name='Customer').exists()
