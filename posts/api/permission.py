from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwernerOrReadOnly(BasePermission):
    message = 'You must be the owner of this..'
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return False


    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user