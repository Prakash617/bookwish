from django.contrib import admin
from . models import PointLogs

# Register your models here.
class PointLogsAdmin(admin.ModelAdmin):
     list_display = ('log_description','user','datetime','log_type')
admin.site.register(PointLogs, PointLogsAdmin)

