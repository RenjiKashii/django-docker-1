from django.contrib.auth.decorators import require_safe, login_required, require_http_methods
from django.shortcuts import render, redirect, get_object_or_404

from . import models, form

@require_safe
def top(request):
    snippets = models.Snippet.objects.all()
    context = {'snippets': snippets}
    return render(request, 'snippets/top.html', context)

@login_required
@require_http_methods(['GET', 'POST', 'HEAD'])
def snippet_new(request):
    if request.method == 'POST':
        form_ = form.SnippetForm(request.POST)
        
        if form_.is_valid():
            snippet = form_.save(commit=False)
            snippet.created_by = request.user
            snippet.save()
            return redirect(snippet_detail, snippet_id=snippet.pk)
    else:
        form_ = form.SnippetForm()
    return render(request, "snippets/snippet_new.html", {'form': form_})

@login_required
def snippet_edit(request, snippet_id):
    snippet = get_object_or_404(models.Snippet, pk=snippet_id)
    if snippet.created_by.id != request.user.id:
        return HttpResponseForbidden("このスニペットの編集は許可されていません。")
    
    if request.method == "POST":
        form_ = form.SnippetForm(request.POST, instance=snippet)
        
        if form_.is_valid():
            form_.save()
            return redirect('snippet_detail', snippet_id=snippet_id)
        else:
            form_ = form.SnippetForm(instance=snippet)
            
        return render(request, 'snippets/snippet_edit.html', {'form': form_})

def snippet_detail(request, snippet_id):
    snippet = get_object_or_404(models.Snippet, pk=snippet_id)
    return render(request, 'snippets/snippet_detail.html',
                  {'snippet': snippet})