from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def home(request,group_name):
    # return HttpResponse('hello')
    group = Group.objects.filter(name = group_name).first()
    chats = []
    if group:
        chats = Chat.objects.filter(group = group)
    else:
        group = Group(name = group_name)
        group.save()
        
    print(group_name)
    return render(request, 'app/index.html',{'group_name':group_name,'chats':chats})