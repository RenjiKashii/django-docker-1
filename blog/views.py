from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .models import Post


class Index(ListView):
    model = Post

class Detail(DetailView):
    model = Post
    
class Create(CreateView):
    model = Post
    
    fields = ["title", "body", "category", "tags"]