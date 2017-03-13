from rest_framework import permissions

class IsOwnerOrNumb(permissions.BasePermission):

	def has_object_permission(self, request, view, obj):
		if request.user:
			return obj.user == request.user
		else:
			return False
