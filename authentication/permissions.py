from rest_framework import permissions


class StudentPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user.user_type == 3

class TeacherPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.user_type == 2

class AdministratorPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.user_type == 1