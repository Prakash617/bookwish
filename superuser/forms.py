from django import forms

from django_summernote.widgets import SummernoteWidget

from website.models import (
    BasicInfo,
    HomepageButton,
    Testimonials,
    Shop,
    CommonQuestion,
    HomeResource,
    Blog,
    Socials,
)

from club.models import Club

class BasicInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm p-2 mb-3'})

    class Meta:
        model = BasicInfo
        fields = "__all__"
        exclude = ('founder_image',)
        labels = {"contact_phone1": "Contact Phone 1","contact_phone2": "Contact Phone 2",}
        widgets = {"founder_message": SummernoteWidget(),
                "founder_bio": SummernoteWidget(),
                "about_us": SummernoteWidget(),
                "about_mission": SummernoteWidget(),
                "about_vision": SummernoteWidget(),
                "privacy_policy": SummernoteWidget(),
                "terms_of_service": SummernoteWidget(),
                "link_and_resources": SummernoteWidget(),
                "helpful_forms": SummernoteWidget(),
                "consultation_request": SummernoteWidget(),
                "services_page": SummernoteWidget(),
                }



class HomepageButtonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm p-2 mb-3'})

    class Meta:
        model = HomepageButton
        fields = "__all__"



class TestimonialCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm p-2 mb-3'})

    class Meta:
        model = Testimonials
        fields = ['name', "message", "intro"]
        exclude = ('picture',)
        labels = {"message": "Testimonial","intro": "Designation or Position","name": "Name of the Person",}
        widgets = {"message": forms.Textarea,}



class CommonQuestionCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm p-2 mb-3'})

    class Meta:
        model = CommonQuestion
        fields = "__all__"
        widgets = {"answer": SummernoteWidget()}



class ShopProductCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm p-2 mb-3'})

    class Meta:
        model = Shop
        fields = "__all__"
        exclude = ('product_photos',)
        widgets = {"product_name":forms.TextInput(attrs={"placeholder": "e.g. Merchaside T-shirt"}), 
                "product_description": forms.Textarea(attrs={"placeholder":"Write a short description about the product.."})
                }
        
        
class CommunityCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm p-2 mb-3'})

    class Meta:
        model = Club
        fields = "__all__"
        # exclude = ('product_photos',)
        # widgets = {"product_name":forms.TextInput(attrs={"placeholder": "e.g. Merchaside T-shirt"}), 
        #         "product_description": forms.Textarea(attrs={"placeholder":"Write a short description about the product.."})}
        # lambda_fields = {'product_name': 'prakash'}



class HomeResourceCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm p-2 mb-3'})

    class Meta:
        model = HomeResource
        fields = "__all__"
        labels = {"iframe_code": "Enter the iframe code from youtube.","name": "Name of the Resource"}


class BlogCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm p-2 mb-3'})
    
    def get_image_url(self):
        if self.cleaned_data.get('feature_image'):
            try:
                # If the file was uploaded through a form, use its temporary file name
                return self.cleaned_data['feature_image'].temporary_file_path()
            except AttributeError:
                # If the file is already saved, use its URL
                return self.cleaned_data['feature_image'].url
    
    class Meta:
        model = Blog
        fields = ["article_title", "article_body", "post_date","feature_image"]
        
        widgets = {
            "article_body": SummernoteWidget(),
            "post_date": forms.SelectDateWidget(),
            }


#-------------------
# Social Medias Forms
class SocialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm p-2 mb-3'})
    
    class Meta:
        model = Socials
        fields = "__all__"
        labels = {"fb_url":"Facebook Url", "in_url":"Instagram Url", "yt_url":"Youtube Url", "app_url":"App Url", "ln_url":"Linkedin Url", }



