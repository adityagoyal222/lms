from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from rest_framework_simplejwt.tokens import RefreshToken


from .models import User, Administrator, Student, Teacher
from .serializers import (UserSerializer, AdministratorSerializer,
                        TeacherSerializer, StudentSerializer)
from .permissions import AdministratorPermission, StudentPermission, TeacherPermission

# Create your views here.
@api_view(['POST'])
def register_admin(request):
    serialized = UserSerializer(data = request.data)
    if(not Administrator.objects.exists()):
        if serialized.is_valid():
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
            administrator = Administrator.objects.create(user = user)
            print(user.password)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "An administrator already exists"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([AdministratorPermission])
def delete_admin(request):
    try:
        print(User.objects.get(username="admin"))
        user = User.objects.get(username="admin")
        admin = Administrator.objects.get(user=user)
        admin.delete()
        user.delete()
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
            print('haha gotcha')
            return Response("Go change yo password")
        else:
            print(user.check_password(request.data.get('password')))
            return Response(get_tokens_for_user(user))
    except:
        return Response("OOPS")

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }