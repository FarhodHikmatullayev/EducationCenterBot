from django.contrib import admin

from .models import *
from .forms import *


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'username', 'role', 'joined_at')
    list_filter = ('joined_at', 'role')
    search_fields = ('full_name', 'username', 'role')
    date_hierarchy = 'joined_at'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'teacher')
    search_fields = ('name', 'teacher__first_name', 'teacher__last_name')


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    form = TeacherProfileForm
    list_display = ('id', 'first_name', 'last_name', 'birth_year', 'experience')
    search_fields = ('first_name', 'last_name')


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    form = ParentProfileForm
    list_display = ('id', 'child_first_name', 'child_last_name', 'user', 'group')
    search_fields = ('child_first_name', 'child_last_name', 'user__full_name', 'group__name')
    list_filter = ('group__name',)



@admin.register(DailyMark)
class DailyMarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'student__group', 'created_at')
    search_fields = ('student__child_first_name', "student__child_last_name", 'student__group__name')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
