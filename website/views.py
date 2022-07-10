from django.shortcuts import render
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "website/index.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
class AboutView(TemplateView):
    template_name = "website/about/index.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
class ContactView(TemplateView):
    template_name = "website/contact/index.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)