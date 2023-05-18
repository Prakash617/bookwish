from django.contrib import admin

from .models import CustomUser, ActiveUser

# admin.site.register(CustomUser)
# admin.site.register(ActiveUser)

class CustomUserAdmin(admin.ModelAdmin):
     list_display = ('username','id','picture','country_code','phone','dob','gender','location','verify_token','email_verified','club','points','physical_badge','mental_badge','emotional_badge','spiritual_badge')
     search_fields =["username","phone","club__club_name"]
admin.site.register(CustomUser, CustomUserAdmin)


class ActiveUserAdmin(admin.ModelAdmin):
     list_display = ('activeUser','date')
     search_fields =["activeUser__username"]

admin.site.register(ActiveUser,ActiveUserAdmin)