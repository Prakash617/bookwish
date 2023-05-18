from django.urls import path
from .views import google_book,GoogleBooksView

urlpatterns = [
    path('superuser/library', google_book, name="googlebook"),
    path('api/library/booklist',GoogleBooksView.as_view(), name = 'api_booklist'),
    

]