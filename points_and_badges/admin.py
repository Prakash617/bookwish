from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register([BookReadingPointTable,PhysicalPointTable,MeditationPointTable,RelationshipPointTable,WeeklyBookReadingPointTable,WeeklyPhysicalPointTable,WeeklyMeditationPointTable,WeeklyRelationshipPointTable])


class BookReadingPointTableAdmin(admin.ModelAdmin):
     list_display = ('date','user','level')
     search_fields = ("user__username","level")
admin.site.register(BookReadingPointTable, BookReadingPointTableAdmin)

class PhysicalPointTableAdmin(admin.ModelAdmin):
     list_display = ('date','user','level')
     search_fields = ("user__username","level")
admin.site.register(PhysicalPointTable, PhysicalPointTableAdmin)


class MeditationPointTableAdmin(admin.ModelAdmin):
     list_display = ('date','user','level')
     search_fields = ("user__username","level")
admin.site.register(MeditationPointTable, MeditationPointTableAdmin)


class RelationshipPointTableAdmin(admin.ModelAdmin):
     list_display = ('date','user','level')
     search_fields = ("user__username","level")
admin.site.register(RelationshipPointTable, RelationshipPointTableAdmin)





class WeeklyBookReadingPointTableAdmin(admin.ModelAdmin):
     list_display = ('date','user','level')
     search_fields = ("user__username","level")
admin.site.register(WeeklyBookReadingPointTable, WeeklyBookReadingPointTableAdmin)

class WeeklyPhysicalPointTableAdmin(admin.ModelAdmin):
     list_display = ('date','user','level')
     search_fields = ("user__username","level")
admin.site.register(WeeklyPhysicalPointTable, WeeklyPhysicalPointTableAdmin)


class WeeklyMeditationPointTableAdmin(admin.ModelAdmin):
     list_display = ('date','user','level')
     search_fields = ("user__username","level")
admin.site.register(WeeklyMeditationPointTable, WeeklyMeditationPointTableAdmin)


class WeeklyRelationshipPointTableAdmin(admin.ModelAdmin):
     list_display = ('date','user','level')
     search_fields = ("user__username","level")
admin.site.register(WeeklyRelationshipPointTable, WeeklyRelationshipPointTableAdmin)



