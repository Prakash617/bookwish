from django.contrib import admin
from .models import *
# Register your models here.
# admin.site.register([Notification,AdminNotification,NotificationTemplate])

# admin.site.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
     list_display = ('sender','revoker','status','picture','notification_type','title','description','upload_timestamp')

admin.site.register(Notification, NotificationAdmin)

class AdminNotificationAdmin(admin.ModelAdmin):
     list_display = ('status','notification_type','title','description','date')
admin.site.register(AdminNotification, AdminNotificationAdmin)

class NotificationTemplateAdmin(admin.ModelAdmin):
     list_display = ('name','template')
admin.site.register(NotificationTemplate, NotificationTemplateAdmin)



