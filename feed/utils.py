import datetime
from user_accounts.models import CustomUser
from .models import  Post
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def is_liked(data,user):
    found = [ True if user == obj["liked_by"]["id"] else False for obj in data]
    if True in found:
        return True
    return False

def get_avg_rating(ratings ,Tusers):
    total = 0
    for rating in ratings:
        print("rating",rating)
        total+= int(rating['rating'])
        
    print('total',total)
    avg = total/Tusers
    return avg

def increase_like_count(post):
    post = Post.objects.get(postId=post)
    current_like_count = post.likes_count
    current_like_count += 1
    post.likes_count = current_like_count
    post.save()

def decrease_like_count(post):
    post = Post.objects.get(postId=post)
    current_like_count = post.likes_count
    current_like_count -= 1
    post.likes_count = current_like_count
    post.save()
    
    
# def generateCommentNotification(userid):
#     print("comment notification",userid)
    # try:
        
    #     if userid.picture == '':
    #         picture = 'https://deejayfarm.com/wp-content/uploads/2019/10/Profile-pic.jpg' 
    #     else:
    #         picture = userid.picture
            
    #     user_obj = CustomUser.objects.get(id=userid.id)
    #     # picture = user_obj.picture
    #     fullName = userid.first_name + " " + userid.last_name
    #     notification = f"{fullName} has liked your post."

    #     return {
    #         "description": notification,
    #         "picture": picture,
    #         "revoker": user_obj,
    #         "title": '',
    #         "upload_timestamp": datetime.datetime.now(),
    #     }
    # except:
    #     return None


# def generateCommentNotification(commented_by, comment_on):
#     print("comment notification",commented_by.id)
#     try:
        
#         if commented_by.picture == '':
#             picture = 'https://deejayfarm.com/wp-content/uploads/2019/10/Profile-pic.jpg' 
#         else:
#             picture = commented_by.picture
            
#         user_obj = CustomUser.objects.get(id=user_obj.id)
#         # print("user_obj",user_obj)
#         # print(picture)
#         # picture = user_obj.picture
#         fullName = commented_by.first_name + " " + commented_by.last_name
#         notification = f"{fullName} has comment your post."
#         # print("fullName", fullName)
#         data =  {
#             "description": notification,
#             "picture": picture,
#             "revoker": user_obj,
#             "title": '',
#             # "upload_timestamp": datetime.datetime.now(),
#         }
#         print('data',data)
#         return data
#     except:
#         return None


def send_mail_daily_report(email,context):
    subject, from_email, to = 'Your Daily Activity', 'from@test.com', email
    html_content = render_to_string('user_accounts/daily_report.html', context) 
    text_content = strip_tags(html_content) 

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
