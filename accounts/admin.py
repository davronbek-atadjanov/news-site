from django.contrib import admin
from .models import Profile
# Register your models here.
# admin.site.register(Profile)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','data_of_birth','photo')
admin.site.register(Profile, ProfileAdmin)
