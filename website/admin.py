from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import (
    Blog,
    BasicInfo,
    HomepageButton,
    ProductQuantity,
    
    Testimonials,
    Shop,
    CommonQuestion,
    HomeResource,
    Order,
    Courses,
    RecommendedArticles,
    RecommendedBooks,
    RecommendedVideos,
    ConsultationRequest,
) 

class BlogAdmin(SummernoteModelAdmin):
    summernote_fields = ('article_body',)

class BasicInfoAdmin(SummernoteModelAdmin):
    summernote_fields = ('founder_message',)

admin.site.register(Blog, BlogAdmin)
admin.site.register(BasicInfo, BasicInfoAdmin)
# admin.site.register(HomepageButton)
# admin.site.register(Testimonials)
# admin.site.register(Shop)
# admin.site.register(CommonQuestion)
# admin.site.register(HomeResource)
# admin.site.register(Order)
# admin.site.register(ProductQuantity)


class TestimonialsAdmin(admin.ModelAdmin):
    list_display = ('picture','intro','name','message',)
admin.site.register(Testimonials,TestimonialsAdmin)

class HomepageButtonAdmin(admin.ModelAdmin):
    list_display = ('name','link')
admin.site.register(HomepageButton,HomepageButtonAdmin)

class ShopAdmin(admin.ModelAdmin):
    list_display = ('product_name','product_description','product_price','quantity','product_photos')
admin.site.register(Shop,ShopAdmin)

class CommonQuestionAdmin(admin.ModelAdmin):
    list_display = ('question','answer')
admin.site.register(CommonQuestion,CommonQuestionAdmin)

class HomeResourceAdmin(admin.ModelAdmin):
    list_display = ('name','iframe_code')
admin.site.register(HomeResource,HomeResourceAdmin)

class ProductQuantityAdmin(admin.ModelAdmin):
    list_display = ('product','quantity')
admin.site.register(ProductQuantity,ProductQuantityAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('get_order_items','order_date','status','payment_type','customer_name','customer_phone','delivery_address','payment_info',)
admin.site.register(Order,OrderAdmin)


class CoursesAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)

class RecommendedArticlesAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)

class RecommendedBooksAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)

class RecommendedVideosAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)





admin.site.register(Courses, CoursesAdmin)
admin.site.register(RecommendedArticles, RecommendedArticlesAdmin)
admin.site.register(RecommendedBooks, RecommendedBooksAdmin)
admin.site.register(RecommendedVideos, RecommendedVideosAdmin)
admin.site.register(ConsultationRequest)