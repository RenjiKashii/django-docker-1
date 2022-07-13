from django.http import HttpResponse
from django.shortcuts import render
from . import models

def top(request):
    snippets = models.Snippet.objects.all()
    context = {'snippets': snippets}
    return render(request, 'snippets/top.html', context)

def snippet_new(request):
    return HttpResponse('スニペット登録')

def snippet_edit(request, snippet_id):
    return HttpResponse('スニペットの編集')

def snippet_detail(request, snippet_id):
    return HttpResponse('スニペットの詳細閲覧')