from django import forms

from django_summernote.widgets import SummernoteWidget


from .models import *

class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm p-2 mb-3'})
    
    class Meta:
        model = Order
        labels = { "customer_name":"Customer Name ", "customer_phone":"Customer Phone ", "delivery_address":"Delivery Address "}
        exclude = (
            'order_item',
            'payment_type',
            'order_date',
            'status',
            'total_price',
            "payment_info"
        )

class CoursesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm p-2 mb-3'})

    def get_image_url(self):
        if self.cleaned_data.get('image'):
            try:
                # If the file was uploaded through a form, use its temporary file name
                return self.cleaned_data['image'].temporary_file_path()
            except AttributeError:
                # If the file is already saved, use its URL
                return self.cleaned_data['image'].url

    class Meta:
        model = Courses
        fields = "__all__"


class RecommendedBooksForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm p-2 mb-3'})


    def get_image_url(self):
        if self.cleaned_data.get('image'):
            try:
                # If the file was uploaded through a form, use its temporary file name
                return self.cleaned_data['image'].temporary_file_path()
            except AttributeError:
                # If the file is already saved, use its URL
                return self.cleaned_data['image'].url

    class Meta:
        model = RecommendedBooks
        fields = "__all__"


class RecommendedArticlesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm p-2 mb-3'})


    def get_image_url(self):
        if self.cleaned_data.get('image'):
            try:
                # If the file was uploaded through a form, use its temporary file name
                return self.cleaned_data['image'].temporary_file_path()
            except AttributeError:
                # If the file is already saved, use its URL
                return self.cleaned_data['image'].url

    class Meta:
        model = RecommendedArticles
        fields = "__all__"


class RecommendedVideosForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm p-2 mb-3'})


    def get_image_url(self):
        if self.cleaned_data.get('image'):
            try:
                # If the file was uploaded through a form, use its temporary file name
                return self.cleaned_data['image'].temporary_file_path()
            except AttributeError:
                # If the file is already saved, use its URL
                return self.cleaned_data['image'].url

    class Meta:
        model = RecommendedVideos
        fields = "__all__"

class ConsultationRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm p-2 mb-3'})

    class Meta:
        model = ConsultationRequest
        fields = "__all__"




class EditAboutUsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm p-2 mb-3'})

    class Meta:
        model = BasicInfo
        fields = "__all__"
        exclude = ('founder_image',"founder_message","founder_bio","about_mission","about_vision","privacy_policy","terms_of_service","link_and_resources","helpful_forms","consultation_request","services_page","contact_phone1","contact_phone2","contact_address","founder_name")
        # labels = {"contact_phone1": "Contact Phone 1","contact_phone2": "Contact Phone 2",}
        widgets = {
                "about_us": SummernoteWidget(),
               
                }
class EditPrivacyPolicyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm p-2 mb-3'})

    class Meta:
        model = BasicInfo
        fields = "__all__"
        exclude = ('founder_image',"founder_message","founder_bio","about_mission","about_vision","about_us","terms_of_service","link_and_resources","helpful_forms","consultation_request","services_page","contact_phone1","contact_phone2","contact_address","founder_name")
        # labels = {"contact_phone1": "Contact Phone 1","contact_phone2": "Contact Phone 2",}
        widgets = {
                "privacy_policy": SummernoteWidget(),
               
                }

class EditTermsofServicesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm p-2 mb-3'})

    class Meta:
        model = BasicInfo
        fields = "__all__"
        exclude = ('founder_image',"founder_message","founder_bio","about_mission","privacy_policy","about_vision","about_us","link_and_resources","helpful_forms","consultation_request","services_page","contact_phone1","contact_phone2","contact_address","founder_name")
        # labels = {"contact_phone1": "Contact Phone 1","contact_phone2": "Contact Phone 2",}
        widgets = {
               "terms_of_service" : SummernoteWidget(),
               
                }
        
class EditLinkandResourcesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm p-2 mb-3'})

    class Meta:
        model = BasicInfo
        fields = "__all__"
        exclude = ('founder_image',"founder_message","founder_bio","about_mission","privacy_policy","about_vision","about_us","terms_of_service","helpful_forms","consultation_request","services_page","contact_phone1","contact_phone2","contact_address","founder_name")
        # labels = {"contact_phone1": "Contact Phone 1","contact_phone2": "Contact Phone 2",}
        widgets = {
                "link_and_resources": SummernoteWidget(),
               
                }
        
class EditConsultationRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm p-2 mb-3'})

    class Meta:
        model = BasicInfo
        fields = "__all__"
        exclude = ('founder_image',"founder_message","founder_bio","about_mission","privacy_policy","about_vision","about_us","terms_of_service","helpful_forms","link_and_resources","services_page","contact_phone1","contact_phone2","contact_address","founder_name")
        # labels = {"contact_phone1": "Contact Phone 1","contact_phone2": "Contact Phone 2",}
        widgets = {
                "consultation_request": SummernoteWidget(),
               
                }
        

class EditSerivicePagesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm p-2 mb-3'})

    class Meta:
        model = BasicInfo
        fields = "__all__"
        exclude = ('founder_image',"founder_message","founder_bio","about_mission","privacy_policy","about_vision","about_us","terms_of_service","helpful_forms","link_and_resources","consultation_request","contact_phone1","contact_phone2","contact_address","founder_name")
        # labels = {"contact_phone1": "Contact Phone 1","contact_phone2": "Contact Phone 2",}
        widgets = {
                "services_page": SummernoteWidget(),
               
                }
        

