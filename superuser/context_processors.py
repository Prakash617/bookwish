from website.models import Socials

def extras(request):
    urls = Socials.objects.all().first()
    return {"urls": urls}