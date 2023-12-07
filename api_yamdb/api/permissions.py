from rest_framework import permissions


class ForAdminOrSurepUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser
        )


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return obj.author == request.user or request.user.role in (
            'admin', 'moderator')
