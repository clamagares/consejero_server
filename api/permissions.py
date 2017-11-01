from rest_framework import permissions

class IsOwner(permissions.BasePermission):
	"""Permission for only grant read and write to the owner of the data"""

	def has_object_permission(self, request, view, obj):
		# Read and write permissions are allowed to any request,
		# so we'll always allow GET, HEAD or OPTIONS requests.
		#if request.method in permissions.SAFE_METHODS:
		#	return True

		# read and write permissions are only allowed to the owner of the snippet.
		return obj.user == request.user