from django.conf.urls import include, url
from rest_framework import urlpatterns
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from authentication.views import register_admin, delete_admin, get_admin

app_name="api"

urlpatterns = [
    url(r'^users/$', get_admin),
    url(r'^users/create/', register_admin),
    url(r'^users/delete/', delete_admin),
    # url(r'^login/', login_user),
    url(r'^token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]