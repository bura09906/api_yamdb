from rest_framework import permissions


<<<<<<< HEAD
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
=======
class ForAdminOrSurepUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser
        )
>>>>>>> 06fa757d5ac21d97808d4410f450044f38d1e127
