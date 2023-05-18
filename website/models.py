import profile
from unicodedata import name
from django.db import models
from django.contrib.postgres.fields import ArrayField
from bs4 import BeautifulSoup

class Testimonials(models.Model):
    picture = models.CharField(max_length=200)
    intro = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    message = models.CharField(max_length=2000)

class BasicInfo(models.Model):
    founder_name = models.CharField(max_length=200, blank=True)
    founder_image = models.ImageField(max_length=400,upload_to='upload/basic_info', blank=True , null = True)
    founder_bio = models.TextField(max_length=200, blank=True)
    founder_message = models.TextField(max_length=9999, blank=True)
    about_us = models.TextField(max_length=99999, blank=True)
    about_mission = models.TextField(max_length=9999, blank=True)
    about_vision = models.TextField(max_length=9999, blank=True)
    
    privacy_policy = models.TextField(max_length=9999, blank=True)
    terms_of_service = models.TextField(max_length=9999, blank=True)
    link_and_resources = models.TextField(max_length=9999, blank=True)
    helpful_forms = models.TextField(max_length=9999, blank=True)
    consultation_request = models.TextField(max_length=9999, blank=True)
    services_page = models.TextField(max_length=9999, blank=True)
    
    contact_phone1 = models.BigIntegerField(blank=True, null=True)
    contact_phone2 = models.BigIntegerField(blank=True, null=True)
    contact_address = models.CharField(max_length=500, blank=True)

class Bookings(models.Model):
    booking_date = models.DateField()
    attendee_name = models.CharField(max_length=200)
    attendee_address = models.CharField(max_length=500)
    ateendee_contact = models.BigIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

class Shop(models.Model):
    product_name = models.CharField(max_length=300, null=True)
    product_description = models.TextField(max_length=999, null=True)
    product_price = models.IntegerField(null=True)
    quantity = models.IntegerField(null=True,blank=True)
    product_photos = ArrayField(
        models.CharField(max_length=3000, blank=True),
        size=3,
    ) 
    def __str__(self):
        return self.product_name

from django.utils import timezone

class Blog(models.Model):
    article_title = models.CharField(max_length=999)
    article_slug = models.CharField(max_length=999)
    feature_image = models.ImageField(max_length=999,upload_to='upload/blog',blank=True ,null= True)
    article_body = models.TextField()
    blog_excerpt = models.CharField(max_length=250, blank=True, null= True)
    # post_date = models.DateField()
    post_date = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.blog_excerpt:
            cleantext = BeautifulSoup(self.article_body, "lxml").text
            self.blog_excerpt = cleantext[:245] + "..."
        return super().save(*args, **kwargs)

class HomepageButton(models.Model):
    name = models.CharField(max_length=999)
    link = models.URLField(max_length=999)

class CommonQuestion(models.Model):
    question = models.CharField(max_length=999)
    answer = models.TextField(max_length=999)

class HomeResource(models.Model):
    name = models.CharField(max_length=300, blank=True)
    iframe_code = models.TextField(max_length=999)

#Social Media Urls
class Socials(models.Model):
    fb_url = models.URLField(max_length=999, blank=True)
    in_url = models.URLField(max_length=999, blank=True)
    yt_url = models.URLField(max_length=999, blank=True)
    app_url = models.URLField(max_length=999, blank=True)
    ln_url = models.URLField(max_length=999, blank=True)

status = (
    ("Approved", "Approved"),
    ("Unapproved", "Unapproved"),
    ("Completed", "Completed"),
    ("Shipped", "Shipped"),
)  

payment_type = (
    ("Cash on Delivery", "Cash on Delivery"),
    ("Online", "Online"),
) 

class ProductQuantity(models.Model):
    product = models.ForeignKey(Shop,on_delete=models.CASCADE, related_name='shop') 
    price = models.FloatField(null=True,blank=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return self.product.product_name
    
countries = (
    ("Nepal", "Nepal"),
    
) 
class Order(models.Model):
    order_item = models.ManyToManyField(ProductQuantity)
    order_date = models.DateField(auto_now_add=True,null=True,blank=True)
    # quantity = models.IntegerField()
    status = models.CharField(max_length=100, choices=status, default="Unapproved")
    total_price = models.FloatField(null=True,blank=True)
    payment_type = models.CharField(max_length=100, choices=payment_type, default="Cash on Delivery")
    customer_name = models.CharField(max_length=999)
    email = models.EmailField(null=True,blank=True)
    customer_phone = models.CharField(max_length=999)
    country = models.CharField(max_length=100,choices=countries,default="Nepal")
    city = models.CharField(max_length=100,null=True,blank=True)
    street =models.CharField(max_length=100,null=True,blank=True)
    delivery_address = models.CharField(max_length=999)
    payment_info = models.JSONField(blank = True,null = True)

    def get_order_items(self):
        return ",".join([str(p) for p in self.order_item.all()])

    @property
    def total(self):
        total = 0
        for order in self.order_item.all():
            total += order.quantity * order.product.product_price
        return total
            
    @property
    def quantity(self):
        total = 0
        for order in self.order_item.all():
            total += order.quantity
        return total


class ActiveUsers(models.Model):
    date = models.DateField()
    active_user_count = models.IntegerField()

class AppInstalls(models.Model):
    date = models.DateField()
    app_installs_count = models.IntegerField()

class Courses(models.Model):
    image = models.ImageField(upload_to='website/course',null=True,blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    time = models.CharField(max_length=100)




class RecommendedBooks(models.Model):
    image = models.ImageField(upload_to='website/course',null=True,blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField(max_length=999, blank=True)

class RecommendedArticles(models.Model):
    image = models.ImageField(upload_to='website/course',null=True,blank=True)
    description = models.TextField()
    link = models.URLField(max_length=999, blank=True)


class RecommendedVideos(models.Model):
    video_link = models.URLField(max_length=999, blank=True)
    description = models.TextField()
    name = models.CharField(max_length=100)
    iframe = models.CharField(max_length=100)

TYPE = (
    ("Personal", "Personal"),
    ("Professional", "Professional"),
)  
class ConsultationRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    company = models.CharField(max_length=999,null=True,blank=True)
    message = models.TextField()
    address = models.CharField(max_length=100)
    type = models.CharField(max_length=999,choices=TYPE,default="Personal") 
