from django.shortcuts import render, redirect

from library.forms import GoogleBooksForm
from .models import GoogleBooks
import requests
from django.contrib import messages
from rest_framework.generics import ListAPIView
from .serializers import GoogleBooksSerializer
from .models import GoogleBooks,CategoryBook
from django.contrib.auth.decorators import login_required,user_passes_test

# Create your views here.
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def google_book(request):
    template_path = "superuser/library.html"
    base_url = 'https://www.googleapis.com/books/v1/volumes/'

    context = {}
    if request.method == "POST":
        if "Submit" in request.POST:
            book_id = request.POST['bookid']
            category = request.POST['category']
           
            new_url = base_url + book_id
            print('new_url',new_url)
            r = requests.get(new_url)
            data = r.json()
            
            try:
                if data['error']['code'] == 503:
                    messages.add_message(request, messages.ERROR, f'Book not available,enter a valid book id')
                    return redirect('googlebook')
            except:            
                GoogleBooks.objects.create(
                    bookid = book_id,
                    category=CategoryBook.objects.get(id=category),
                )
            return redirect('googlebook')
           


        elif "delete_book" in request.POST:
            id = request.POST['book_id']
            d = GoogleBooks.objects.get(bookid = id)
            
            d.delete()

    context['book_data']=[]
    books = GoogleBooks.objects.all()
    
    for book in books:
        new_url = base_url + book.bookid
        r = requests.get(new_url)
        data = r.json()
    
        context['book_data'].append({'id':data['id'],'title':data["volumeInfo"]["title"],'category': book.category})
        print(context['book_data'])
        # title = data["volumeInfo"]["title"]
    
    # print(r.json())
    context['form'] = GoogleBooksForm()
    return render(request, template_path,context)


class GoogleBooksView(ListAPIView):
    serializer_class = GoogleBooksSerializer
    queryset = GoogleBooks.objects.all()


