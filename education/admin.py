from django.contrib import admin

from .models import *
from .forms import *


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'username', 'role')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'teacher')


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    form = TeacherProfileForm
    list_display = ('id', 'first_name', 'last_name', 'birth_year', 'experience')


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    form = ParentProfileForm
    list_display = ('id', 'child_first_name', 'child_last_name', 'group')


@admin.register(DailyMark)
class DailyMarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'created_at')
