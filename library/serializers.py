from .models import GoogleBooks,CategoryBook
from rest_framework import serializers


class GoogleBooksSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    # def to_representation(self,instance):
    #     response = super().to_representation(instance)
    #     response['category_name'] = CategoryBook.objects.filter(name=instance.category)

        # return response 
    class Meta:
        model = GoogleBooks
        fields = ('id','bookid','category_name')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'bookid': data['bookid'],
            'category_name': data['category_name']
        }