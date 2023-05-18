from django.db import models

# Create your models here.
class CategoryBook(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class GoogleBooks(models.Model):
    category = models.ForeignKey(CategoryBook,on_delete=models.CASCADE)
    bookid = models.CharField(max_length=100)

    def __str__(self):
        return self.bookid
