import random
from django.shortcuts import render, redirect
import requests
from datetime import datetime as dt
from django.contrib import messages
from user_accounts.models import CustomUser
# from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from rest_framework.authtoken.models import Token

from superuser.utils import get_BookReading, get_DailyStepCount, get_relations,delete_image_from_url
from user_accounts.utils import send_refer_code
from bookwishes.settings import DEBUG,ip
from django.db.models.functions import TruncMonth
from django.db.models import Count
from datetime import datetime
from .utils import users_by_month
from django.shortcuts import get_object_or_404
from event_app.models import Event
from django.shortcuts import render
from django.shortcuts import render, redirect



from .forms import (
    BasicInfoForm,
    HomepageButtonForm,
    TestimonialCreationForm,
    ShopProductCreationForm,
    CommonQuestionCreationForm,
    HomeResourceCreationForm,
    BlogCreationForm,
    SocialForm,
    CommunityCreationForm,
    
)

from user_accounts.models import (
    CustomUser,
    ActiveUser,
)

from notification.models import AdminNotification, Notification

from feed.models import(
    Story,
    Post,
    Comment,
)

from club.models import(
    Club,
    DailyStepCount,
    BookReading,
    PostReport,
    StoryReport,
    Relationship,
    Refer,
    CommentReport,
)

from website.models import (
    BasicInfo,
    HomepageButton,
    Order,
    Testimonials,
    Shop,
    CommonQuestion,
    HomeResource,
    Blog,
    Socials,
)

from django.core.files.storage import FileSystemStorage

#for cloudinary





from datetime import date
from django.db.models.functions import TruncMonth
# Create your views here.
@login_required(login_url='login')
def superuser(request):
    template_path = "superuser/superuser.html"
    context = {}

    user_url = ip + 'auth/users/'
    r = requests.get(user_url)
    first_day = date.today().replace(day=1)
    # print(dt.now().date())
    if request.user.is_superuser:
        total_users = len(r.json())

        total_stories = Story.objects.filter(upload_timestamp = dt.now().date()).count()
        total_active_users = ActiveUser.objects.filter(date=date.today()).count()
        # get_total_users_by_today_month
        total_active_users_month = ActiveUser.objects.filter(date__gte=first_day).annotate(
                                                                month=TruncMonth('date')
                                                            ).values('month').annotate(
                                                                count=Count('id')
                                                            ).order_by('month').aggregate(
                                                                total_count=Sum('count')
                                                            )['total_count']
        total_posts_today = Post.objects.filter(postdate = dt.now().date()).count()
        total_clubs = Club.objects.all().count()
        distance = DailyStepCount.objects.filter(record_date = dt.now().date())
        steps = get_DailyStepCount(distance)
        step = round(steps,2)
        books = BookReading.objects.filter(record_date = dt.now().date())
        pages = get_BookReading(books)
        relations = Relationship.objects.filter(record_date = dt.now().date())
        neg_points,pos_points = get_relations(relations)
        total_post_today = Post.objects.filter(postdate = dt.now().date()).count()
        

        club_exist = False        
        try:
            club = Club.objects.get(club_owner = request.user)
            club_exist = True
        except:
            pass
        context["pages"] = pages
        context["step"] = step        
        context["club_exist"] = club_exist    
        context["pos_points"] = pos_points
        context["neg_points"] = neg_points

        context["total_users"] = total_users
        context["total_stories"] = total_stories
        context["total_clubs"] = total_clubs
        context["total_active_users"] = total_active_users
        context["total_active_users_month"] = total_active_users_month
        context["total_posts_today"] = total_posts_today

        

    else:
        total_stories = Story.objects.filter(upload_timestamp = dt.now().date(), posted_club = request.user.club ).count()
        total_posts_today = Post.objects.filter(postdate = dt.now().date(),posted_club = request.user.club).count()
        distance = DailyStepCount.objects.filter(record_date = dt.now().date(),userid__club = request.user.club)
        relations = Relationship.objects.filter(record_date = dt.now().date(),userid__club = request.user.club)
        books = BookReading.objects.filter(record_date = dt.now().date(),userid__club = request.user.club)
        pages = get_BookReading(books)
        neg_points,pos_points = get_relations(relations)        
        step = get_DailyStepCount(distance)
        # print(total_stories)
        total_users= CustomUser.objects.filter(club= request.user.club).count()
        total_active_users = ActiveUser.objects.filter(activeUser__club=request.user.club).count()
        context["pages"] = pages
        context["step"] = step  
        context["total_users"] = total_users
        context["total_stories"] = total_stories
        context["total_posts_today"] = total_posts_today
        context["total_active_users"] = total_active_users
        context["pos_points"] = pos_points
        context["neg_points"] = neg_points

    return render(request, template_path, context)



@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def superuser_settings(request):
    template_path = "superuser/settings.html"
    context = {}
    
    basic_info = BasicInfo.objects.all().first()
    homepage_button = HomepageButton.objects.all().first()

    if request.method == "POST":
        if "basic_info_submit" in request.POST:
            current_form = BasicInfoForm(request.POST, instance=basic_info)

            if current_form.is_valid:
                current_form.save()
                return redirect('superuser_settings')
        
        if "homepage_button_submit" in request.POST:
            current_button_form = HomepageButtonForm(request.POST, instance=homepage_button)

            if current_button_form.is_valid:
                current_button_form.save()
                return redirect('superuser_settings')
    
        if "homepage_image_button_submit" in request.POST:
            image_file = request.FILES["homepage_image"]
            print(image_file)
            try:
                
                try:
                    current_website_data = BasicInfo.objects.all().first()
                   
                    current_website_data.founder_image = image_file
                    current_website_data.save()
                        
                except:
                    founder_image, created = BasicInfo.objects.create(founder_image=image_file)
                    print("error to save image")
                    # current_website_data  = BasicInfo.objects.create(founder_image = url)
                
                
                return redirect('superuser_settings')

            except:
                context["error"] = "Please upload images less than 10mb."
                return render(request,template_path, context)
    
    form1 = BasicInfoForm(instance=basic_info)
    context["form1"] = form1

    form2 = HomepageButtonForm(instance=homepage_button)
    context["form2"] = form2

    return render(request, template_path, context)




@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def testimonial_admin(request):
    template_path = "superuser/testimonials.html"
    context = {}

    if request.method == "POST":
        if "new_testimonial_submit" in request.POST:
            received_testimonial_data = TestimonialCreationForm(request.POST)
            if request.FILES:
                received_image = request.FILES["picture"]
            else:
                received_image = None
            
            if received_testimonial_data.is_valid:
                if received_image is not None:
                    fss = FileSystemStorage()
                    file = fss.save(received_image.name, received_image)
                    file_url = fss.url(file)
                else:
                    # 561115
                    # dummy image needs to changed with it's own server image in production
                    file_url = 'https://res.cloudinary.com/mediaholic-nepal/image/upload/v1662358025/Soprada/elements_and_icons/avatar_qmku46.jpg'

                current_form_data = received_testimonial_data.save(commit=False)
                current_form_data.picture = file_url
                current_form_data.save()
                
                return redirect('testimonial_admin')
            else:
                context["testimonial_error"] = "You did not enter a valid testimonial data."

    testimonial_creation_form = TestimonialCreationForm()
    context["testimonial_form"] = testimonial_creation_form

    testimonial_data = Testimonials.objects.all()
    context["all_testimonials"] = testimonial_data

    return render(request, template_path, context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def delete_testimonial(request, id):
    current_testimonial = Testimonials.objects.get(pk=id)
    current_testimonial.delete()
    return redirect('testimonial_admin')





@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def shop_admin(request):
    template_path = "superuser/shop.html"
    context = {}

    if request.method == "POST":

        if "product_submit" in request.POST:
            current_product = ShopProductCreationForm(request.POST)

            if request.FILES:
                photos = request.FILES.getlist("product_pictures")
            else:
                photos = None
            # print('photos', photos)
            if current_product.is_valid:
                # current_product.save()
                if photos is None:
                    # print('None')
                    # url = ['/media/default-image/empty.png']
                    url = ["https://therevivalists.com/admin/fm/source/empty.png"]

                    p=current_product.save(commit=False)
                    p.product_photos = url
                    p.save()
                    return redirect("shop_admin")
                url = []
                if photos is not None:
                    if len(photos) <= 3 and len(photos) >= 1:
                        file_uploader = FileSystemStorage()
                        for item in photos:
                            file = file_uploader.save(item.name, item)
                            url.append(file_uploader.url(file))
                        print('url',url)

                        product_upload_data = current_product.save(commit=False)
                        product_upload_data.product_photos = url
                        product_upload_data.save()
                        return redirect("shop_admin")

                    else:
                        context["product_error"] = "You are not allowed to upload more than 3 pictures for a product"
                else:
                
                    context["product_error"] = "You need to upload at least one photo for the product."
                
                
            else:
                context["product_error"] = "You did not enter a valid product data."


    all_product_list = Shop.objects.all()
    context["all_products"] = all_product_list

    product_form = ShopProductCreationForm()
    context["product_form"] = product_form
    
    return render(request, template_path, context)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def delete_product(request, id):
    current_product = Shop.objects.get(pk=id)
    current_product.delete()
    return redirect('shop_admin')



@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def common_questions_admin(request):
    template_path = "superuser/common-questions.html"
    context = {}

    if request.method == "POST":
        if "common_question_submit" in request.POST:
            current_question_answer = CommonQuestionCreationForm(request.POST)
            if current_question_answer.is_valid():
                current_question_answer.save()
                return redirect("common_questions_admin")

    form = CommonQuestionCreationForm()
    context["form"] = form
    
    questions = CommonQuestion.objects.all()
    context["questions"] = questions

    return render(request, template_path, context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def delete_common_question(request, id):
    CommonQuestion.objects.get(pk=id).delete()
    return redirect("common_questions_admin")



@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def home_resources_admin(request):
    template_path = "superuser/resources-home.html"
    context = {}

    if request.method == "POST":
        if "resources_submit" in request.POST:
            form_data = HomeResourceCreationForm(request.POST)
            if form_data.is_valid:
                form_data.save()
                return redirect("home_resources_admin")

    all_resources = HomeResource.objects.all()
    context["all_resources"] = all_resources

    resource_form = HomeResourceCreationForm()
    context["resource_form"] = resource_form

    return render(request, template_path, context)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def delete_home_resources_item(request,id):
    HomeResource.objects.get(pk=id).delete()
    return redirect("home_resources_admin")


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def blogpost_admin(request):
    template_path = "superuser/blogpost.html"
    blogs = Blog.objects.all().order_by('-id')
    context = {
        'blogs': blogs,
    }
    for blog in blogs:
        if blog.feature_image:
            blog.feature_image_url = blog.feature_image.url
        else:
            blog.feature_image_url = ''
    
    
    return render(request, template_path, context)

def filter_reportStory(story_report):
    
    filtered_story_report = [person for person in people if condition(person)]
    
    return filtered_story_report
    
    
    
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def storyReport_admin(request):
    template_path = "superuser/StoryReportSection/storyReport.html"
    context = {}
    context['data'] = []
    
    details= StoryReport.objects.all()
    story_report = []
    reported_by = []
    report_category = []
    story  = []
    for s in details:
        
        if s.story not in story:
            story.append(s.story)
            # context['reported_by'].append(d.reported_by.get_full_name())
            story_report.append(s)
            # report_category = d.report_category
            reported_bys = StoryReport.objects.filter(story=s.story)
            for r in reported_bys:
                reported_by.append(r.reported_by.get_full_name())
            report_categorys = StoryReport.objects.filter(report_category=s.report_category)
            for r in reported_bys:
                report_category.append(r.report_category.name)
            print('report_category',report_category)
            # reported_by.append.reported_by.get_full_name()
            # report_category.append.report_category.name
            current_data = {

                'story_report': story_report,
                'reported_by': reported_by,
                'report_category': report_category,
                # 'report_category': set(report_category),
                
                
            }   
            context['data'].append(current_data)
            reported_by = []
            report_category = []
            story_report = []
            
        else: 
            pass
        
    print('data',context)
    # context["details"]  = details
    return render(request, template_path, context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def postReport_admin(request):
    template_path = "superuser/reportSection/postReport.html"
    context = {}
    context['data'] = []
    
    details= PostReport.objects.all()
    # details= StoryReport.objects.all()
    post_report = []
    reported_by = []
    report_category = []
    post  = []
    for s in details:
        
        if s.post not in post:
            post.append(s.post)
            # context['reported_by'].append(d.reported_by.get_full_name())
            post_report.append(s)
            # report_category = d.report_category
            reported_bys = PostReport.objects.filter(post=s.post)
            for r in reported_bys:
                reported_by.append(r.reported_by.get_full_name())
            report_categorys = StoryReport.objects.filter(report_category=s.report_category)
            for r in reported_bys:
                report_category.append(r.report_category.name)
            print('report_category',report_category)
            # reported_by.append.reported_by.get_full_name()
            # report_category.append.report_category.name
            current_data = {

                'post_report': post_report,
                'reported_by': reported_by,
                'report_category': report_category,
                # 'report_category': set(report_category),
                
                
            }   
            context['data'].append(current_data)
            reported_by = []
            report_category = []
            post_report = []
            
        else: 
            pass
        
    print('data',context)
    # context["details"]  = details
    return render(request, template_path, context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def commentReport_admin(request):
    template_path = "superuser/commentReport/commentReport.html"
    context = {}
    context["details"] = []
    for cr in CommentReport.objects.all():
        
        comment_obj = Comment.objects.get(pk=cr.comment.id)
        postMedia = comment_obj.post.postMedia
        print(comment_obj.post.postMedia)
        cr_obj = {
            "cr_obj":cr ,
            "postMedia":postMedia
        }
        context['details'].append(cr_obj)
  
    return render(request, template_path, context)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
#Creating Blog Posts
def create_blog_admin(request):
    context = {}
    template_path = "superuser/create_blogpost.html"
    form = BlogCreationForm()
    context["form"] = form
    
    if request.method == "POST":
        # POST = request.POST.copy()
        # image_file = POST.pop("post_image")
        form = BlogCreationForm(request.POST,request.FILES)
        print('helloe')
        # print('file created')
        # print(request.FILES)
        # print('request.FILES["post_image"]',request.FILES["post_image"])
        # try:
        #     image_file = request.FILES["post_image"] 
        # except:
        #     image_file = None
        #     print('file not uploaded')
        # try:   
        #     if image_file:
        #         uploaed_file_data = cloudinary.uploader.upload(image_file,folder="Bookwishes/website/images",format='jpg')
        #         url = uploaed_file_data['secure_url'] 
        #     else:
        #         url = ""
        #     print('url',url)
            # print(url)
        # try:
        if form.is_valid():
            
            # image_url = form.get_image_url()
            title = form.cleaned_data["article_title"]
            # body = form.cleaned_data["article_body"]
            # date = form.cleaned_data["post_date"]
            # form.save()
            # feature_image = form.get_image_url()
            # print('image_url',image_url)

            # feature_image = form.cleaned_data["feature_image"]
            # feature_image = form.get_image_url()
            # print('feature_image',newform.feature_image)
            
            slug_t = ""
            for i in title:
                if  i == '.':
                    i = ""
                if i == " ":
                    i = "-"
                slug_t += i
            
            # Blog.objects.create(
            #     article_title = title,
            #     article_slug = slug_t,
            #     feature_image = feature_image,
            #     article_body = body,
            #     post_date = date,
            # )
            newform = form.save(commit=False)
            newform.article_slug = slug_t
            newform.save()
        return redirect("blogpost_admin")
        # except:
        #     print("Error")
            
    return render(request, template_path, context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def edit_blogpost(request, b_id):
    context = {}
    template_path = "superuser/edit_blogpost.html"
    blogpost = Blog.objects.get(id = b_id)
    form = BlogCreationForm(instance = blogpost)
    context["blogpost_form"] = form

    if request.method == "POST":
        blogpost = Blog.objects.get(id = b_id)
        form = BlogCreationForm(request.POST, instance = blogpost)
        if form.is_valid():
            form.save()
            return redirect("blogpost_admin")

    return render(request, template_path, context)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def delete_blogpost(request, b_id):
    # context = {}
    # template_path = ""
    blogpost_data = Blog.objects.get(id = b_id)
    blogpost_data.delete()

    return redirect("blogpost_admin")

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def delete_order(request, b_id):
    # context = {}
    # template_path = ""
    order_data = Order.objects.get(id = b_id)
    order_data.delete()

    return redirect("shop-data")

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def set_order_complete(request, b_id):
    # context = {}
    # template_path = ""
    order = Order.objects.get(id = b_id)
    order.status = "Completed"
    
    # order_data.delete()
    order.save()
    print("Order completed successfully")

    return redirect("shop-data")

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def delete_blogstory(request, b_id):
    # context = {}
    # template_path = ""
    print("Delete")
    blogpost_data = Story.objects.get(id = b_id)
    blogpost_data.delete()

    return redirect("blogpost_admin")



@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def delete_postReport(request, b_id):
    print("enter post report")
    try:
        postReport_data = PostReport.objects.get(id = b_id).post
        post = Post.objects.get(postId = postReport_data.postId)
        image_url = post.postMedia
        
        # print("Post Report", postReport_data)
        post.delete()
        try:
            delete_image_from_url(image_url)
        except:
            pass
        return redirect("post_report")
    except:
        return redirect("post_report")
    
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def delete_commentReport(request, b_id):
    # context = {}
    # template_path = ""
    try:
        commentReport_data = CommentReport.objects.get(id = b_id).comment
        comment = Comment.objects.get(id = commentReport_data.id)
        # print("Post Report", postReport_data)
        comment.delete()
        return redirect("comment_report")
    except:
        return redirect("comment_report")
    
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def delete_story_report(request, b_id):
    # context = {}
    # template_path = ""
    print('jie')
    try:
        # post = Story.objects.get(postId = b_id)
        storyReport_data = StoryReport.objects.get(id = b_id).story
        story = Story.objects.get(id = storyReport_data.id)
        print("Post Report", story)
        image_url = story.media
        story.delete()
        try:
            delete_image_from_url(image_url)
        except:
            pass
        return redirect("story_report")
    except:
        return redirect("story_report")
    
@login_required(login_url='login')
def delete_post(request, b_id):
    # context = {}
    # template_path = ""
    
    try:
        post = Post.objects.get(postId = b_id,postedBy=request.user)
        # story = Story.objects.get(id = storyReport_data.id)
        # print("Post Report", story)
        post.delete()
        return redirect("upload-a-feed")
    except:
        return redirect("upload-a-feed")
from feed.models import Media
@login_required(login_url='login')
def delete_media(request, b_id):
    # context = {}
    # template_path = ""
    
    try:
        media = Media.objects.get(id = b_id)
        # story = Story.objects.get(id = storyReport_data.id)
        # print("media Report", story)
        media.delete()
        return redirect("media")
    except:
        return redirect("media")
    
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def delete_notification(request, b_id):
    # context = {}
    # template_path = ""
    
    try:
        post = AdminNotification.objects.get(id = b_id)
        # story = Story.objects.get(id = storyReport_data.id)
        # print("Post Report", story)
        post.delete()
        return redirect("notifications-admin")
    except:
        return redirect("notifications-admin")

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
#Edit Social Media Urls
def edit_socials(request):
    template_path = "superuser/edit_socials.html"
    context = {}
    socials = Socials.objects.all().first()
    
    Socials_form = SocialForm(instance=socials)

    context['Socials_form'] = Socials_form


    if request.POST:
        socials = Socials.objects.all().first()
        form = SocialForm(request.POST, instance=socials)
        if form.is_valid():
            form.save()
            return redirect("superuser_settings")

    return render(request, template_path, context)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def website_traffic(request):
    template_path = "superuser/traffic.html"
    context = {}
    total_active_users = ActiveUser.objects.all().count()
    context["total_active_users"] = total_active_users
    return render(request, template_path, context)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def website_analytics(request):
    template_path = "superuser/analytics.html"
    gender_counts = {'Male' : 0, 'Female': 0, 'NA': 0}
    context = {}
    total_active_users = ActiveUser.objects.all().count()
    context["total_active_users"] = total_active_users

    #Counting number of genders
    user_url = ip + 'auth/users/'
    r = requests.get(user_url, auth=('user', 'pass'))
    data = r.json()
    # print("data",data)
    for d in data:
        if d['gender'] != None :
            for gender in gender_counts.keys():
                if d['gender'] == gender:
                    gender_counts[gender] += 1
    # gender_counts['Male'] = 
    context['gender_counts'] = gender_counts
    
    context["users_by_month"] = users_by_month(CustomUser)
    # print(gender_counts)

    #Counting number of Users according to their age
    age_counts = [0,0,0,0,0,0,0]
    for d in data:
        if d['dob'] != None:
            todays_date = str(dt.now().date())
            # print(todays_date)
            user_age = int((
                dt.strptime(todays_date, "%Y-%m-%d") - dt.strptime(d['dob'], "%Y-%m-%d")
            ).days/365)

            if user_age >=0  and user_age < 10:
                age_counts[0] += 1
            elif user_age >=10  and user_age < 20:
                age_counts[1] += 1
            elif user_age >=20  and user_age < 30:
                age_counts[2] += 1
            elif user_age >=30  and user_age < 40:
                age_counts[3] += 1
            elif user_age >=40  and user_age < 50:
                age_counts[4] += 1
            elif user_age >=50  and user_age < 60:
                age_counts[5] += 1
            else:
                age_counts[6] += 1
    context['age_counts'] = age_counts
    # print('age_counts',age_counts)

    return render(request, template_path, context)


from django.db.models import Sum
from datetime import date

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def shop_data(request):
    template_path = "superuser/shop-data.html"
    context = {}
    orders = Order.objects.all()
    total_order = orders.count()


    if request.method == "POST":
        order_id = request.POST["order_id"]
        order_status = request.POST["status"]

        try:
            current_order = Order.objects.get(id=order_id)
            current_order.status = order_status
            current_order.save()
        except:
            pass

        return redirect("shop-data")

    # orders = Order.objects.all()
    total_revenue = 0
    today_total_revenue = 0
    total_order_price = 0
    for order in orders:
        total_order_price = order.total
        if order.status == 'Completed':
            total_revenue += order.total
            
    today = date.today()
    today_order = Order.objects.filter(order_date= today)
    
    today_total_order = today_order.count()
    
    for order in today_order:
        if order.status == 'Completed':
            today_total_revenue += order.total
    
    
    # print(order)
    context['orders'] = orders
    context['total_order_price'] = total_order_price
    context['total_order'] = total_order
    context['total_revenue'] = total_revenue
    context['today_total_order'] = today_total_order
    context['today_total_revenue'] = today_total_revenue
    return render(request, template_path, context)


from django.contrib.auth.models import User
from django.db.models.functions import TruncMonth
from django.db.models import Count
from datetime import datetime
from .utils import club_by_month


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def bookwishes_communities(request):
    template_path = "superuser/community.html"
    context = {}

    total_clubs = Club.objects.all().count()

    clubs = Club.objects.all()

    context["data"] = []
    post_count = 0
    neg_points = 0
    pos_points = 0
    
    for c in clubs:
        total_steps = 0
        neg_points = 0
        pos_points = 0
        total_read_pages = 0
        Custom_user = CustomUser.objects.filter(club=c.club_id)
        post= Post.objects.filter(posted_club=c.club_id)
        post_count=post.count()
        member_count = Custom_user.count()
        
        for u in Custom_user:
          dc = DailyStepCount.objects.filter(userid=u.id).aggregate(total=Sum("distance"))
          sum = dc['total'] if dc['total'] else 0
          total_steps += sum
          from django.db.models import  IntegerField, F
          from django.db.models.functions import Cast

          read_pages = BookReading.objects.filter(userid=u.id).annotate(read_pages=Cast(F('end_page') - F('start_page'),  output_field=IntegerField())
        ).aggregate(total = Sum('read_pages'))

          page = read_pages['total'] if read_pages['total'] else 0
          total_read_pages += page

          neg_point = Relationship.objects.filter(userid=u.id).aggregate(total = Sum("neg_points"))
          negs = neg_point['total'] if neg_point['total'] else 0
          neg_points += negs
          pos_point = Relationship.objects.filter(userid=u.id).aggregate(total = Sum("plus_points"))       
          pos = pos_point['total'] if pos_point['total'] else 0
          pos_points += pos
        


        
        current_data = {
                'club_id':c.club_id,
                'name': c.club_name,
                'total_members': member_count,
                'total_posts': post_count,
                'total_steps': total_steps,
                'total_pages': total_read_pages,
                'neg_points': neg_points,
                'plus_points': pos_points
            }
        
        context["data"].append(current_data)
        # print('context["data"]',context["data"])

    context["total_clubs"] = total_clubs
    context["club_by_month"] = club_by_month(Club)
    
    # Community-form
    community_form = CommunityCreationForm()
    context["community_form"] = community_form
    if request.method == "POST":
            try:
                if "community_submit" in request.POST:
                    current_community = CommunityCreationForm(request.POST)
                    if current_community.is_valid:
                        current_club=current_community.save()
                        user = CustomUser.objects.get(id=current_club.club_owner.id)
                        user.club = current_club
                        user.save()
                        context["community_error"] =  "Successfully Created"
            
                pass
            except:
                context["community_error"] = "You did not enter a valid community data."
    return render(request, template_path, context)
# from django.contrib.auth.models import User

@login_required(login_url='login')
def user_management(request):
    template_path = "superuser/user_management.html"
    context = {}
    user_url = ip + 'auth/users/'
    r = requests.get(user_url)
    
    if request.user.is_superuser:
        total_users = len(r.json())
        users = r.json()
        # print('users',users)
        context["users_by_month"] = users_by_month(CustomUser)

    else:
        club_user = CustomUser.objects.all()
        total_users = club_user.filter(club=request.user.club).count()
        users = club_user.filter(club=request.user.club)
    context["total_users"] = total_users
    context["users"] = users
    update_user = []
    user_refer = {}
    for u in users :
        if request.user.is_superuser:
            # print('json',u['id'])
            user = CustomUser.objects.get(id=u['id'])
        else:
            user = CustomUser.objects.get(id=u.id)
            # print('query_set',u.id)
        refer = Refer.objects.filter(onboarded_user=user).values('refer_code').first()['refer_code'] if Refer.objects.filter(onboarded_user=user).exists() else 'None'
        
        user_refer['user'] = user
        user_refer['refer'] = refer
        update_user.append(user_refer.copy())
        
    context['update_user'] = update_user
    context["total_active_users"] = ActiveUser.objects.all().count()
    return render(request, template_path, context)


@login_required(login_url='login')
def club_management(request):
    template_path = "superuser/user_management.html"
    context = {}
    # club_user = Club.objects.filter(club_owner = request.user)
    total_users = CustomUser.objects.filter(club=request.user.club).count()
    context["total_users"] = total_users

    user_url = ip + 'auth/users/'
    r = requests.get(user_url, auth=('user', 'pass'))

    users = r.json()
    # print(users)
    context["users"] = users
    for u in users :
        user = CustomUser.objects.get(id=u['id'])
        print(user.id)
        try:
            refer = Refer.objects.get(onboarded_user = user)
            # print("Ayo AYo")
            print(refer)
        except:
            print("Ayena AYena")
            refer = None
        u['refer'] = refer

    context["total_active_users"] = ActiveUser.objects.all().count()
    return render(request, template_path, context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def notifications_admin(request):
    template_path = "superuser/notifications.html"
    context = {}
    if request.method == "POST":
        if "send_notification" in request.POST:
            msg = request.POST.get('message')
            print(msg)
            user = request.user
            
            AdminNotification.objects.create(
                # sender = user,
                status = 'Sent',
                notification_type = 'admin',
                title = msg,
                description = msg
            )
            print('not running notification')
            return redirect("notifications-admin")
        elif "delete_notification" in request.POST:
            print(request.POST["notifictaion_id"])
            ids = request.POST["notifictaion_id"]
            d = AdminNotification.objects.get(id=ids)
            d.delete()
           
            
    all_notifications = AdminNotification.objects.all()
    context['notifications'] = all_notifications

    return render(request, template_path, context)

@login_required(login_url='login')
def upload_a_feed(request):
    template_path = "superuser/upload_feed.html"
    context = {}
 
    if request.method == "POST":
        
        print(request.FILES)
        # image_file = request.POST.get('post_image')
        
        
        try:
            # upload_file_data = cloudinary.uploader.upload(image_file,folder="Bookwishes/website/images",format='jpg')
            # print("uploaed_file_data",upload_file_data['secure_url'])
            try:
                image_file = request.FILES["post_image"]
                Post.objects.create(postedBy = request.user,posted_club = request.user.club,postDescription = request.POST.get('post_description'),
                                    # postMedia = upload_file_data['secure_url'],
                                    postMedia=image_file
                                    )
                
                # print('created')
                context['msg'] = 'post upload'
                return redirect('upload-a-feed')
            except:
                Post.objects.create(postedBy = request.user,posted_club = request.user.club,postDescription = request.POST.get('post_description'))
                
                # print('created')
                context['msg'] = 'post upload'
                return redirect('upload-a-feed')
        except: 
            context['msg'] = 'post upload error'
            return redirect('upload-a-feed')
           
    posts = Post.objects.filter(postedBy=request.user)
    # print(posts)
    context['posts'] = posts
    
    return render(request, template_path, context)
    

@login_required(login_url='login')
def upload_a_feed(request):
    template_path = "superuser/upload_feed.html"
    context = {}
 
    if request.method == "POST":
        
        print(request.FILES)
        # image_file = request.POST.get('post_image')
        
        
        try:
            # upload_file_data = cloudinary.uploader.upload(image_file,folder="Bookwishes/website/images",format='jpg')
            # print("uploaed_file_data",upload_file_data['secure_url'])
            try:
                image_file = request.FILES["post_image"]
                Post.objects.create(postedBy = request.user,posted_club = request.user.club,postDescription = request.POST.get('post_description'),
                                    # postMedia = upload_file_data['secure_url'],
                                    postMedia=image_file
                                    )
                
                # print('created')
                context['msg'] = 'post upload'
                return redirect('upload-a-feed')
            except:
                Post.objects.create(postedBy = request.user,posted_club = request.user.club,postDescription = request.POST.get('post_description'))
                
                # print('created')
                context['msg'] = 'post upload'
                return redirect('upload-a-feed')
        except: 
            context['msg'] = 'post upload error'
            return redirect('upload-a-feed')
           
    posts = Post.objects.filter(postedBy=request.user)
    # print(posts)
    context['posts'] = posts
    
    return render(request, template_path, context)
    
    
    
    # return render(request, template_path, context)

def sent_refer_email(request,email_list,lenght):
    print("SentReferEmailRefer")
    context = {'response': {},}
    template_path = "superuser/refer.html"
    context['lenght'] = lenght
    print(lenght)
    for item in email_list:
        if Refer.objects.filter(generated_for=item).exists():
            context['response'][item] = "Error Sending email"
            messages.add_message(request, messages.ERROR, f'{item} Error Sending email')

        else:
            referred_by = request.user
            onboarded_user = None
            
            
            generated = True
            while generated:
                try:
                    refer_code = "BW" + str(random.randint(100011, 999999))
                    refer = Refer.objects.create(referred_by=referred_by, onboarded_user=onboarded_user, refer_code=refer_code, generated_for=item)
                    try:
                        send_refer_code(refer_code, item)
                    except:
                        generated = False
                        messages.add_message(request, messages.INFO, f'Email Sent Complete')

                    break
                except:
                    print("done")
                    generated = False
                    # break

            context['response'][item] = 'Email Sent'
            messages.add_message(request, messages.SUCCESS, f'{lenght}-Email Sent successfully')
            

    return render(request, template_path, context)
    
import re

@login_required(login_url='login')
def refer_user(request):
    template_path = "superuser/refer.html"
    context = {'response': {},}

    if request.method == "POST":
        # send emails all the list of email received
        print(request.POST)
        if "csv_submit" in request.POST:
            # print(request)
            csv_file = request.FILES["csv_file"]
            # print(csv_file)
            file_data = csv_file.read().decode('utf-8')
            print('file_data',file_data)
            # formatter_fn = lambda sentence: re.sub(r'([^\s\w\.])+', '', sentence).lower()
            csv_data  = file_data.split('\n')
            csv_data_len = len(csv_data)
          
            email_list = []
            pattern = r'\r'
            # for x in csv_data:
            #     email_list.append(x.split(','))
                # fields = x.split(',')
                # print(fields[0])
                # print(fields[1])
            for email in csv_data:
                if email == "":
                    pass
                else:
                    email_list.append(re.sub(pattern, '', email) )
           
            sent_refer_email(request,email_list,csv_data_len-1)
            
            
        elif 'send_refer_code' in request.POST:
            email_data = request.POST['email-submission-list']
            email_list = email_data.split(',')
            lenght = len(email_list)
            context['lenght'] = lenght
            print(email_list)
            sent_refer_email(request,email_list,lenght)
            
            return render(request, template_path, context)
        
    return render(request, template_path, context)

def superuser_login(request):
    template_path = "login/login.html"
    context = {}
    
    if request.user.is_authenticated:
         return redirect("superuser")

    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        # print(username, password)
        user = authenticate(request, username=username, password=password)
        # print(user)
        try:
            club = Club.objects.get(club_owner = user)
        except:
            club = {} 
         
        try:
            is_superuser = user.is_superuser | False
        except:
            is_superuser = False
        # print(is_superuser)          
 
        if is_superuser or club:
            login(request, user)
            return redirect("superuser")
        
        else:
           pass

    return render(request, template_path, context)


def superuser_logout(request):
    logout(request)
    return redirect("login")




# Add event from superuser
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def add_event(request):
    if request.method == 'POST':
        event = Event(
            event_name=request.POST.get('event_name'),
            event_start_time=request.POST.get('event_start_time'),
            event_end_time=request.POST.get('event_end_time'),
            event_start_date=request.POST.get('event_start_date'),
            event_end_date=request.POST.get('event_end_date'),
            event_topic=request.POST.get('event_topic'),
            event_location=request.POST.get('event_location'),
            picture=request.FILES.get('picture'),
            description=request.POST.get('description'),
            participant_numbers=request.POST.get('participant_numbers'),
            event_location_link=request.POST.get('event_location_link')
        )
        event.save()
        return redirect('add_event')
    else:
        events = Event.objects.all()
        return render(request, 'superuser/add_event.html', {'events': events})
    
# delete events from superuser
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('add_event')

