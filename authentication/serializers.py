from rest_framework import serializers

from .models import User, Administrator, Teacher, Student

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'user_type')
        

# Optional Serializer for PUT request 
# class RestrictedUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'user_type' 'password', 'first_name', 'last_name')
#         extra_kwargs = {
#             'first_name': {"required": False},
#             'last_name': {"required": False},
#             'username': {"read_only": True},
#             'email': {"read_only": True},
#             'user_type': {"read_only": True}
#         }

class AdministratorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Administrator
        fields = ('id', 'user')

class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ('id', 'user')

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ('id', 'user')

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)