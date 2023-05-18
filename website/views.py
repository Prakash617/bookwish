from .forms import OrderForm
from rest_framework.permissions import IsAuthenticated
from .utils import send_consultation_request_email, send_order_email
import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import json
from .models import (
    BasicInfo,
    HomepageButton,
    Testimonials,
    Shop,
    HomeResource,
    Socials,
    Blog,
    Order,
    CommonQuestion,ProductQuantity,Courses,RecommendedArticles,RecommendedBooks,
    RecommendedVideos,
    ConsultationRequest,
)
from .forms import *
from django.template import Template, Context
from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from bookwishes.settings import ip

# Create your views here.


def home(request):
    template_path = 'website/index.html'
    context = {}

    founder_data = BasicInfo.objects.all().first()
    # print('hello',founder_data.founder_image)
    context["founder_data"] = founder_data

    homepage_button_data = HomepageButton.objects.all().first()
    context["button_data"] = homepage_button_data

    testimonials_data = Testimonials.objects.all()
    context["testimonials_data"] = testimonials_data

    resources_data = HomeResource.objects.all()
    context["resources"] = resources_data

    # Social Media Urls
    socials = Socials.objects.all().first()
    context["socials"] = socials

    return render(request, template_path, context)


def about(request):
    template_path = "website/about.html"
    context = {}
    basic_info = BasicInfo.objects.first()
    about_us = basic_info.about_us
    context["about_us"] = about_us
    return render(request, template_path, context)


def services_page(request):
    template_path = "website/services.html"
    context = {}
    courses = Courses.objects.all()
    context["courses"] = courses
    basic_info = BasicInfo.objects.first()
    services_page = basic_info.services_page
    final_context = {}
    final_context["services_page"] = Template(services_page).render(Context(context))

    return render(request, template_path, final_context)
        

def blog(request):
    template_path = "website/blog/archive.html"
    context = {}
    context['top_blog'] = Blog.objects.all()[:1]
    context['blogs'] = Blog.objects.all()[1:]
    return render(request, template_path, context)


def blogpost(request, id, slug):
    context = {}
    blogdetails = Blog.objects.get(id=id)
    context["blog"] = blogdetails
    template_path = "website/blog/single.html"
    return render(request, template_path, context)


def helpful_forms(request):
    template_path = "website/helpful-forms.html"
    context = {}
    basic_info = BasicInfo.objects.first()
    helpful_forms = basic_info.helpful_forms
    context["helpful_forms"] = helpful_forms
    return render(request, template_path, context)


def consultation_request(request):
    template_path = "website/consultation_request.html"
    context = {}
    basic_info = BasicInfo.objects.first()
    consultation_request = basic_info.consultation_request

    if request.method == "POST":
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken')

        new_data = {}
        for k,v in data.items():
            new_data[k] = v
        
        

        
        send_consultation_request_email(new_data)
       
        ConsultationRequest.objects.create(**new_data)
        return redirect('consultation-request')

    
    context["consultation_request"] = Template(consultation_request).render(Context())
    return render(request, template_path,context)

def resources(request):
    template_path = "website/resources.html"
    context = {}
    basic_info = BasicInfo.objects.first()
    recommended_article =RecommendedArticles.objects.all()
    recommended_book = RecommendedBooks.objects.all()
    recommended_videos = RecommendedVideos.objects.all()
    # template
    link_and_resources_html = basic_info.link_and_resources
    
    # context
    context["recommended_article"] = recommended_article
    context["recommended_book"] = recommended_book
    context["recommended_videos"] = recommended_videos

    template = Template(link_and_resources_html)
    context_data = Context(context)

    link_and_resources = template.render(context_data)
    final_context = {}
    final_context["link_and_resources"] = link_and_resources
    
    return render(request, template_path,final_context)

def faqs(request):
    template_path = "website/faqs.html"
    context = {}
    questions = CommonQuestion.objects.all()
    for q in questions:
        print(q)
    context["questions"] = questions
    print(context["questions"])
    return render(request, template_path, context)


def shop(request):
    template_path = 'website/shop/archive.html'
    context = {}

    shop_products = Shop.objects.all()
    context["shop_products"] = shop_products

    # Serialize the dictionary to JSON
    shop_products_json = json.dumps(list(shop_products.values()))

    # Pass the serialized JSON to the template context
    context['shop_products_json'] = shop_products_json

    return render(request, template_path, context)


def cart(request):
    template_path = "website/shop/cart.html"
    context = {}
    orders = Order.objects.all()
    context['orders'] = orders

    # total_price = 0
    # for o in orders:
    #     total_price += o.quantity * o.order_item.price
    # context['total_price'] = total_price

    return render(request, template_path, context)


def privacy_policy(request):
    template_path = "website/privacy-policy.html"
    context = {}
    basic_info = BasicInfo.objects.first()
    privacy_policy = basic_info.privacy_policy
    context["privacy_policy"] = privacy_policy
    return render(request, template_path, context)


def terms_and_conditions(request):
    template_path = "website/terms_and_conditions.html"
    context = {}
    basic_info = BasicInfo.objects.first()
    terms_and_conditions = basic_info.terms_of_service
    context["terms_and_conditions"] = terms_and_conditions
    return render(request, template_path, context)


# def transform_data(data):
#     result = {}
#     total = 0
#     for obj in data:
#         total += obj['product.product_price']
#         if obj['product.id'] in result:
#             result[obj['product.id']]['quantity'] += 1
#         else:
#             result[obj['product.id']] = {'quantity': 1, **obj}
#     # print('total',total)

#     result['total_price'] = total

#     print("===============================================================================================")
#     return list(result.values())


def checkoutdetail(request):
    template_path = "website/checkoutdetail.html"
    context = {}
    if request.method == 'POST':
        print('hit the checkout')
        order_item = request.POST['order_item']
        customer_name = request.POST['customer_name']
        customer_phone = request.POST['customer_phone']
        email =request.POST['email']
        country =request.POST['country']
        city =request.POST['city']
        street =request.POST['street']

        delivery_address = request.POST['delivery_address']
        payment_info = {"empty":"empty"}
        # print(order_item)
        data = transform_data(json.loads(order_item))
        cart_data = transform_data(json.loads(order_item))
        total_price = cart_data.pop()
        print('total',total_price)
        order = Order.objects.create(order_date=datetime.date.today())


        for item in cart_data:
            product = Shop.objects.get(id=item['id'])
            productquantity = ProductQuantity.objects.create(
                product=product, quantity=item['quantity'], price=item['product_price'])
            order.order_item.add(productquantity)

        order.total_price = total_price['grand_total']

        order.customer_name = customer_name
        order.customer_phone = customer_phone
        order.delivery_address = delivery_address
        order.country = country
        order.city = city
        order.street = street
        order.email = email
        order.payment_info = payment_info
        order.save()
        print("""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")
        print(data)
        send_order_email(email, data, delivery_address)

        return redirect('/shop')
    else:
        form = OrderForm()

    form = OrderForm()
    context["form"] = form
    context["ip"] = ip
    return render(request, template_path, context)


@login_required(login_url='login')
def courses(request):
    template_path = "website/courses.html"
    context = {}

    if request.method == "POST":
        if "Submit" in request.POST:

        
        # image_file = request.POST.get('image')

            try:
                # upload_file_data = cloudinary.uploader.upload(image_file,folder="Bookwishes/website/images",format='jpg')
                # print("uploaed_file_data",upload_file_data['secure_url'])
                try:
                    image_file = request.FILES["image"]
                    Courses.objects.create(image=image_file, name=request.POST.get('name'), time=request.POST.get('time'), description=request.POST.get('description')
                                        )

                    # print('created')
                    context['msg'] = 'course upload'
                    return redirect('course')
                except:
                    Courses.objects.create(name=request.POST.get('name'), time=request.POST.get('time'), description=request.POST.get('description')
                                            )

                    context['msg'] = 'course upload'
                    return redirect('course')
            except:
                context['msg'] = 'course upload error'
                return redirect('course')
        
        elif "delete_course" in request.POST:
            id = request.POST['course_id']
            d = Courses.objects.get(id = id)
            d.delete()
            return redirect('course')

    courses = Courses.objects.all()
    context["form"] = CoursesForm()
   
    context['courses'] = courses

    return render(request, template_path, context)




@login_required(login_url='login')
def recommended_book(request):
    template_path = "website/recommendedbook.html"
    context = {}

    if request.method == "POST":
        if "Submit" in request.POST:

            print(request.FILES)
            # image_file = request.POST.get('image')

            try:
                # upload_file_data = cloudinary.uploader.upload(image_file,folder="Bookwishes/website/images",format='jpg')
                # print("uploaed_file_data",upload_file_data['secure_url'])
                try:
                    image_file = request.FILES["image"]
                    RecommendedBooks.objects.create(image=image_file, name=request.POST.get('name'), link=request.POST.get('link'), description=request.POST.get('description')
                                        )

                    # print('created')
                    context['msg'] = 'book upload'
                    return redirect('book')
                except:
                    RecommendedBooks.objects.create(link=request.POST.get('link'), description=request.POST.get('description')
                                        )

                context['msg'] = 'book upload'
                return redirect('book')
            except:
                context['msg'] = 'book upload error'
                return redirect('book')
        
        elif "delete_book" in request.POST:
            id = request.POST['book_id']
            d = RecommendedBooks.objects.get(id=id)
            
            d.delete()
            return redirect('book')
        

    books = RecommendedBooks.objects.all()
    context['books'] = books
    context['form'] = RecommendedBooksForm()

    return render(request, template_path, context)

@login_required(login_url='login')
def recommended_article(request):
    template_path = "website/recommendedArticle.html"
    context = {}

    if request.method == "POST":
        if "Submit" in request.POST:

                print(request.FILES)
                # image_file = request.POST.get('image')

                try:
                    # upload_file_data = cloudinary.uploader.upload(image_file,folder="Bookwishes/website/images",format='jpg')
                    # print("uploaed_file_data",upload_file_data['secure_url'])
                    try:
                        image_file = request.FILES["image"]
                        RecommendedArticles.objects.create(image=image_file, link=request.POST.get('link'), description=request.POST.get('description')
                                            )

                        # print('created')
                        context['msg'] = 'article upload'
                        return redirect('article')
                    except:
                       RecommendedArticles.objects.create(link=request.POST.get('link'), description=request.POST.get('description')
                                            )

                    context['msg'] = 'article upload'
                    return redirect('article')
                except:
                    context['msg'] = 'article upload error'
                    return redirect('article')
                
        elif "delete_article" in request.POST:
            id = request.POST['article_id']

            d = RecommendedArticles.objects.get(id = id)
            
            d.delete()
            return redirect('article')

    articles = RecommendedArticles.objects.all()
    context['articles'] = articles
    context['form'] = RecommendedArticlesForm()


    return render(request, template_path, context)



@login_required(login_url='login')
def recommended_videos(request):
    template_path = "website/recommendedvideo.html"
    context = {}

    if request.method == "POST":
        if "Submit" in request.POST:

                print(request.FILES)
                # image_file = request.POST.get('image')
                current_link = request.POST.get('video_link')
                new_link = current_link.replace('watch?v=', 'embed/')
                try:
                    # upload_file_data = cloudinary.uploader.upload(image_file,folder="Bookwishes/website/images",format='jpg')
                    # print("uploaed_file_data",upload_file_data['secure_url'])
                        RecommendedVideos.objects.create(name=request.POST.get('name'), video_link=request.POST.get('video_link'), description=request.POST.get('description'),iframe=new_link)
                        context['msg'] = 'video upload'
                        return redirect('video')
                except:
                    context['msg'] = 'video upload error'
                    return redirect('video')
                
        elif "delete_video" in request.POST:
            id = request.POST['video_id']

            d = RecommendedVideos.objects.get(id = id)
            
            d.delete()
            return redirect('video')


    videos = RecommendedVideos.objects.all()
    context['videos'] = videos
    context["form"] = RecommendedVideosForm()

    return render(request, template_path, context)

@login_required(login_url='login')
def consultation_request_admin(request):
    template_path = "website/consultation_request_admin.html"
    context = {}
    if request.method == "POST":
         id = request.POST['consult_id']

         d = ConsultationRequest.objects.get(id = id)
            
         d.delete()
         return redirect('admin_consultation_request')


        
    consulation_request = ConsultationRequest.objects.all()
    context['consulation_requests'] = consulation_request

    return render(request, template_path, context)

def pages(request):
    template_path = "website/pages.html"
    return render(request, template_path)




def edit_service_pages(request):
    template_path = "website/edit_pages.html"
    context = {}
    basic_info = BasicInfo.objects.all().first()
    if request.method == "POST":
        basic_info.services_page = request.POST.get('services_page')
        basic_info.save()
        redirect("pages")

    context["form"] = EditSerivicePagesForm({
        "services_page": basic_info.services_page
    })
    return render(request, template_path, context)

def edit_privacy_policy(request):
    template_path = "website/edit_pages.html"
    context = {}
    basic_info = BasicInfo.objects.all().first()
    if request.method == "POST":
        basic_info.privacy_policy = request.POST.get('privacy_policy')
        basic_info.save()
        redirect("pages")

    context["form"] = EditPrivacyPolicyForm({
        "privacy_policy": basic_info.privacy_policy
    })
    return render(request, template_path, context)

def edit_aboutus(request):
    template_path = "website/edit_pages.html"
    context = {}
    basic_info = BasicInfo.objects.all().first()
    if request.method == "POST":
        basic_info.about_us = request.POST.get('about_us')
        basic_info.save()
        redirect("pages")

    context["form"] = EditAboutUsForm({
        "about_us": basic_info.about_us
    })
    return render(request, template_path, context)

def edit_consultation_request(request):
    template_path = "website/edit_pages.html"
    context = {}
    basic_info = BasicInfo.objects.all().first()
    if request.method == "POST":
        basic_info.consultation_request = request.POST.get('consultation_request')
        basic_info.save()
        redirect("pages")

    context["form"] = EditConsultationRequestForm({
        "consultation_request": basic_info.consultation_request
    })
    return render(request, template_path, context)

def edit_link_and_resources(request):
    template_path = "website/edit_pages.html"
    context = {}
    basic_info = BasicInfo.objects.all().first()
    if request.method == "POST":
        basic_info.link_and_resources = request.POST.get('link_and_resources')
        basic_info.save()
        redirect("pages")

    context["form"] = EditLinkandResourcesForm({
        "link_and_resources": basic_info.link_and_resources
    })
    return render(request, template_path, context)

def edit_terms_and_services(request):
    template_path = "website/edit_pages.html"
    context = {}
    basic_info = BasicInfo.objects.all().first()
    if request.method == "POST":
        basic_info.terms_of_service = request.POST.get('terms_of_service')
        basic_info.save()
        redirect('pages')

    context["form"] = EditTermsofServicesForm({
        "terms_of_service": basic_info.terms_of_service
    })

    return render(request, template_path, context)


def transform_data(data):
    new_data = []
    summary_data = {}
    delivery = 'Free'
    grand_total = 0 
    total_quantity = 0
    for d in data:
        # Check if product already exists in new_data
        product_exists = False
        for nd in new_data:
            if d['id'] == nd['id']:
                nd['quantity'] += 1
                nd['total'] += d['product_price']
                product_exists = True
                break
        if not product_exists:
            # Add quantity field if product does not exist in new_data
            d['quantity'] = 1
            d['total'] = d['product_price']
            new_data.append(d)
            
    for item in new_data:
        grand_total += item['quantity'] * item['product_price']
        total_quantity += item['quantity']
        
        
    order_len = len(new_data)
    summary_data['total_items'] = total_quantity
    summary_data['grand_total'] = grand_total
    summary_data['delivery'] = delivery
    new_data.append(summary_data)
    print('new_data:', new_data)
    return new_data



# class SentCheckoutMail(ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     lookup_field = 'id'
#     permission_classes = [IsAuthenticated]

#     def list(self, request, *args, **kwargs):
        
        
#         # data = request.data

#         # data = request.data.get('order_items')
#         # email = request.data.get('email')

#         # print(data)

#         # order_items=transform_data(data)

#         return Response({'info': "success"})

#     def create(self, request, *args, **kwargs):
#         print("=====================================")
#         data = request.data
#         email = request.data.get('email')
#         data = request.data.get('order_items')
#         address = request.data.get('address')
#         order_items = transform_data(data)
#         send_order_email(email, order_items, address)
#         return Response({'info': "success"})

from feed.models import Media

@login_required(login_url='login')
def media(request):
    template_path = "website/media.html"    
    context = {}
    
    if request.method == "POST":
        print('hit the POST method')
        print(request.FILES)
        files = request.FILES.getlist('post_images[]')
        for file in files:
            media = Media.objects.create(media=file,name=file.name,alt=file.name)
            
        return redirect('media')
    
    medias = Media.objects.all()
    # medias = Media.objects.all().order_by("-created")
    
    context['medias'] = medias
    
    return render(request, template_path, context)


# event registraion
from event_app.models import EventRegistration 
from event_app.models import Event, EventViews

def event_registration(request):
    template_path = "website/events/event_registration.html"

    context = {}
    event_uuid = request.GET.get('event')
    event = Event.objects.get(event_uuid=event_uuid)
    registrations_count = EventRegistration.objects.filter(event=event).count()

    # event views
    try:
        current_event = EventViews.objects.get(event = event)
        current_event.view_count += 1
        current_event.save()
    except EventViews.DoesNotExist:
        EventViews.objects.create(event = event, view_count = 1)
        

    context["event"] = event
    context["registrations_count"] = registrations_count


    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
       
        try:
            already_registeted_user = EventRegistration.objects.get(email=email, event=event)

            if already_registeted_user:
                context['error'] = "You have already registered for this event."
                return render(request, template_path, context)
        except:
            registration = EventRegistration(name=name, email=email, phone=phone,
                                         event=event,location=location,
                                         dob=dob, gender=gender)
            registration.save()
            print(registration)
            context["success"] = "You have successfully registered for the event."
            return render(request, template_path, context)
            

    
    
       
    return render(request, template_path, context)


# event attendance
def event_attendance(request):
    template_path = "website/events/event_attendance.html"

    context = {}
    uuid = request.GET.get('event')
    event_data = Event.objects.get(event_uuid=uuid)
    context["event_data"] = event_data
   
    if request.method == 'POST':
        post_email = request.POST.get('email')
        
        event_registrations = EventRegistration.objects.filter(email=post_email, event=event_data)

        for registration in event_registrations:
            registration.attended = True
            registration.save()
            print(f"{post_email} has been marked as attended")
            context["success"] = "You have successfully checked in."
            return render(request, template_path, context)

#
        
        if not event_registrations:
            context['error'] = "Unable to find your registration details."
            print(f"No registration found for {post_email}")
            return render(request, template_path, context)

    
        
    return render(request, template_path, context)




# class SentCheckoutMail(ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     lookup_field = 'id'
#     permission_classes = [IsAuthenticated]

#     def list(self, request, *args, **kwargs):
        
        
#         # data = request.data

#         # data = request.data.get('order_items')
#         # email = request.data.get('email')

#         # print(data)

#         # order_items=transform_data(data)

#         return Response({'info': "success"})

#     def create(self, request, *args, **kwargs):
#         print("=====================================")
#         data = request.data
#         email = request.data.get('email')
#         data = request.data.get('order_items')
#         address = request.data.get('address')
#         order_items = transform_data(data)
#         send_order_email(email, order_items, address)
#         return Response({'info': "success"})

from feed.models import Media

@login_required(login_url='login')
def media(request):
    template_path = "website/media.html"    
    context = {}
    
    if request.method == "POST":
        print('hit the POST method')
        print(request.FILES)
        files = request.FILES.getlist('post_images[]')
        for file in files:
            media = Media.objects.create(media=file,name=file.name,alt=file.name)
            
        return redirect('media')
    
    medias = Media.objects.all()
    # medias = Media.objects.all().order_by("-created")
    
    context['medias'] = medias
    
    return render(request, template_path, context)
