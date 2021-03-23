from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


from .models import User, Administrator, Student, Teacher
from .serializers import (UserSerializer, AdministratorSerializer,
                        TeacherSerializer, StudentSerializer, ChangePasswordSerializer)
from .permissions import AdministratorPermission, StudentPermission, TeacherPermission

# Create your views here.
@api_view(['POST'])
def register_admin(request):
    serialized = UserSerializer(data = request.data)
    if(not Administrator.objects.exists()):
        if serialized.is_valid():
            if request.data.get("user_type") == 1:
                user = User.objects.create(
                    username = request.data.get('username'),
                    email = request.data.get('email'),
                    first_name = request.data.get('first_name'),
                    last_name = request.data.get('last_name'),
                    user_type = request.data.get('user_type'),
                    password = make_password(request.data.get('password')) + "_NEW",
                )
                # user.set_password(request.data.get('password'))
                # user.save()
                administrator = Administrator.objects.create(user = user)
                return Response(serialized.data, status=status.HTTP_201_CREATED)
            else:
                return Response("Can only register an admin")
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "An administrator already exists"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([AdministratorPermission])
def delete_admin(request):
    try:
        user = User.objects.get(username=request.data.get('username'))
        if user.user_type == 1:
            admin = Administrator.objects.get(user=user)
            admin.delete()
            user.delete()
        else:
            return Response({"error": "Can only delete a teacher"})
    except:
        return Response({"error": "The user does not exist"})
    else:
        return Response({"success": "The user was deleted"})

@api_view(['GET'])
def get_admin(request):
    user = list(User.objects.filter(user_type=1).values("username", "email", "first_name", "last_name", "user_type"))
    admin = list(Administrator.objects.values("user_id"))
    return JsonResponse({"data": {"admin": admin, "user": user}})

@api_view(['POST'])
def login_user(request):
    try:
        user = User.objects.get(username=request.data.get('username'))
        if(user.password[-4:] == "_NEW"):
            return Response("Go change yo password")
        else:
            if user.check_password(request.data.get('password')):
                return Response(get_tokens_for_user(user))
            else:
                return Response("Wrong password")
    except:
        return Response("OOPS")

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AdministratorPermission])
def register_student(request):
    serialized = UserSerializer(data = request.data)
    if serialized.is_valid():
        if request.data.get("user_type") == 3:
            user = User.objects.create(
                username = request.data.get('username'),
                email = request.data.get('email'),
                first_name = request.data.get('first_name'),
                last_name = request.data.get('last_name'),
                user_type = request.data.get('user_type'),
                # password = make_password(request.data.get('password')) + "_NEW",
            )
            user.set_password(request.data.get('password'))
            user.save()
            student = Student.objects.create(user = user)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response("Can only register a student")
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([AdministratorPermission])
def delete_student(request):
    try:
        user = User.objects.get(username=request.data.get('username'))
        if user.user_type == 3:
            student = Student.objects.get(user=user)
            student.delete()
            user.delete()
        else:
            return Response({"error": "Can only delete a teacher"})
    except:
        return Response({"error": "The user does not exist"})
    else:
        return Response({"success": "The user was deleted"})

@api_view(['GET'])
def get_student(request):
    user = list(User.objects.filter(user_type=3).values("username", "email", "first_name", "last_name", "user_type"))
    student = list(Student.objects.values("user_id"))
    return JsonResponse({"data": {"student": student, "user": user}})

@api_view(['POST'])
@permission_classes([AdministratorPermission])
def register_teacher(request):
    serialized = UserSerializer(data = request.data)
    if serialized.is_valid():
        if request.data.get("user_type" == 2):
            user = User.objects.create(
                username = request.data.get('username'),
                email = request.data.get('email'),
                first_name = request.data.get('first_name'),
                last_name = request.data.get('last_name'),
                user_type = request.data.get('user_type'),
                # password = make_password(request.data.get('password')) + "_NEW",
            )
            user.set_password(request.data.get('password'))
            user.save()
            teacher = Teacher.objects.create(user = user)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response("Can only register a teacher")
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([AdministratorPermission])
def delete_teacher(request):
    try:
        user = User.objects.get(username=request.data.get('username'))
        if user.user_type == 2:
            teacher = Teacher.objects.get(user=user)
            teacher.delete()
            user.delete()
        else:
            return Response({"error": "Can only delete a teacher"})
    except:
        return Response({"error": "The teacher does not exist"})
    else:
        return Response({"success": "The teacher was deleted"})

@api_view(['GET'])
def get_teacher(request):
    user = list(User.objects.filter(user_type=2).values("username", "email", "first_name", "last_name", "user_type"))
    teacher = list(Teacher.objects.values("user_id"))
    return JsonResponse({"data": {"teacher": teacher, "user": user}})
    