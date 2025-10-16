from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'mobile', 'gender']
    list_filter = ['gender']
    search_fields = ['user__username', 'user__email']