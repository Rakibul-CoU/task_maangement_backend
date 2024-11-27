from django.contrib import admin

from api.models import CustomUser, Task

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active', 'is_staff', 'is_verified', 'phone_number')

admin.site.register(CustomUser, CustomUserAdmin)


admin.site.register(Task, TaskAdmin)