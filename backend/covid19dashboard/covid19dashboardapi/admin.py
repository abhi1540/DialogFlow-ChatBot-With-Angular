from django.contrib import admin
from .models import CustomUser,CustomUserAdmin, Userconv

#admin.site.unregister(CustomUser)
admin.site.register(CustomUser, CustomUserAdmin)
admin.register(Userconv)