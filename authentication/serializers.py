from rest_framework import serializers

from .models import User, Administrator, Teacher, Student

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'user_type')


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