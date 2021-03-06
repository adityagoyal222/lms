from django.conf.urls import include, url
from rest_framework import urlpatterns
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from authentication.views import (register_admin, delete_admin,
                                get_admin, login_user,
                                ChangePasswordView, register_student,
                                delete_student, get_student,
                                register_teacher, delete_teacher,
                                get_teacher)

app_name="api"

urlpatterns = [
    url(r'^admin/$', get_admin),
    url(r'^admin/create/', register_admin),
    url(r'^admin/delete/', delete_admin),
    url(r'^student/$', get_student),
    url(r'^student/create/', register_student),
    url(r'^student/delete/', delete_student),
    url(r'^teacher/$', get_teacher),
    url(r'^teacher/create/', register_teacher),
    url(r'^teacher/delete/', delete_teacher),
    url(r'^login/', login_user),
    url(r'^token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^change-password/', ChangePasswordView.as_view(), name='change-password'),
    url(r'^password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset'))
]