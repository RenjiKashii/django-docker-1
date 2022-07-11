from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from .models import Post


class Index(ListView):
    model = Post

class Detail(DetailView):
    model = Post
    
class Create(CreateView):
    model = Post
    
    fields = ["title", "body", "category", "tags"]

class Update(UpdateView):
    model = Post
    fields = ["title", "body", "category", "tags"]
    
class Delete(DeleteView):
    model = Post
    
    # 削除したあとに移動する先（トップページ）
    success_url = "/blog"