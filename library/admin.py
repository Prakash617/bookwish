from django.contrib import admin
from .models import GoogleBooks,CategoryBook
# from django.contrib.auth.models import Group
# admin.site.register([GoogleBooks,CategoryBook])
# from rest_framework.authtoken.models import TokenProxy
# Register your models here.
class GoogleBooksAdmin(admin.ModelAdmin):
    list_display = ('bookid', 'category')
    search_fields = ('bookid', 'category__name')

admin.site.register(GoogleBooks, GoogleBooksAdmin)

class CategoryBookAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(CategoryBook, CategoryBookAdmin)


# from django.apps import apps

# # Get a list of all the models in your app
# models = apps.get_models()
# # admin.site.unregister(TokenProxy)

# # Create a generic ModelAdmin class that displays all fields
# class AllFieldsModelAdmin(admin.ModelAdmin):
#     list_display = [field.name for model in models for field in model._meta.fields]

# # Register all the models with the generic ModelAdmin class
# for model in models:
    
    
    
      
#     admin.site.register(model, AllFieldsModelAdmin)
    
#     # print(model._meta.app_label)
#     # if (model._meta.app_label == 'library'):
#     #     print(model)
#     #     admin.site.register(model, AllFieldsModelAdmin)