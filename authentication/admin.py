from django.contrib import admin
from .models import User, Administrator, Student, Teacher

# Register your models here.
admin.site.register(User)
admin.site.register(Administrator)
admin.site.register(Student)
admin.site.register(Teacher)