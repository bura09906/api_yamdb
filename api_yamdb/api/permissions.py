from rest_framework import permissions


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
