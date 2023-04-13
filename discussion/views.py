from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_safe, require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.core.paginator import Paginator
# from django.db.models import Count
from datetime import date, timedelta

from .models import Posting, Comment, Reply
from .forms import PostingForm, CommentForm, ReplyForm

# Create your views here.

@login_required
@require_http_methods(['GET', 'POST'])
def posting_create(request):
    if request.method == 'POST':
        form = PostingForm(request.POST)
        if form.is_valid():
            posting = form.save(commit=False)
            posting.author = request.user
            posting.save()
            return redirect('discussion:posting_detail', posting.pk)
    else:
        form = PostingForm()
    
    return render(request, 'discussion/form.html', {
        'form': form,
    })

@require_safe
def posting_index(request):
    postings = Posting.objects.order_by('created_at')
    paginator = Paginator(postings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'discussion/index.html', {
        'page_obj':page_obj,
    })

@login_required
@require_safe
def posting_feed(request):
    user = request.user
    postings = Posting.objects.filter(author__in=user.followings.all())  # 작동 여부 확인 필요.
    # postings = Posting.objects.filter(created_at__lte = date.today() - timedelta(days=7))

    return render(request, 'discussion/index.html', {
        'postings': postings,
    })

@require_safe
def posting_detail(request, posting_pk):
    
    posting = get_object_or_404(Posting, pk=posting_pk)
    comments = posting.comment_set.all()
    
    form = CommentForm()
    is_best = posting.users_best.filter(pk=request.user.pk).exists()
    is_worst = posting.users_worst.filter(pk=request.user.pk).exists()
    
    return render(request, 'discussion/detail.html', {
        'posting': posting,
        'comments': comments,
        'form': form,
        'is_best': is_best,
        'is_worst': is_worst,
    })

@login_required
@require_http_methods(['GET', 'POST'])
def posting_update(request, posting_pk):
    posting = get_object_or_404(Posting, pk=posting_pk)

    if request.user != posting.author:
        return redirect('discussion:posting_index') 

    if request.method == 'POST':
        form = PostingForm(request.POST, instance=posting)
        if form.is_valid():
            posting = form.save()
            return redirect('discussion:posting_detail', posting.pk)

    else:
        form = PostingForm(instance=posting)
    
    return render(request, 'discussion/form.html', {
        'form':form,
    })

@login_required
@require_POST
def posting_delete(request, posting_pk):
    posting = get_object_or_404(Posting, pk=posting_pk)

    if request.user != posting.author:
        return redirect('discussion:posting_index')

    posting.delete()

    return redirect('discussion:posting_index')

@login_required
@require_POST
def posting_best(request, posting_pk):
    user = request.user
    posting = get_object_or_404(Posting, pk=posting_pk)

    if posting.users_best.filter(pk=user.pk).exists(): 
        posting.users_best.remove(user)
    
    else:
        posting.users_best.add(user)

    return redirect('discussion:posting_detail', posting.pk)

@login_required
@require_POST
def posting_worst(request, posting_pk):
    user = request.user
    posting = get_object_or_404(Posting, pk=posting_pk)

    if posting.users_worst.filter(pk=user.pk).exists():
        posting.users_worst.remove(user)

    else:
        posting.users_worst.add(user)

    return redirect('discussion:posting_detail', posting.pk)

@login_required
@require_POST
def comment_create(request, posting_pk):
    posting = get_object_or_404(Posting, pk=posting_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.posting = posting
        comment.author = request.user
        comment.save()
        return redirect('discussion:posting_detail', posting.pk)
    else:
        return HttpResponseBadRequest('Can not proceed.')

@login_required
@require_http_methods(['GET', 'POST'])
def comment_update(request, posting_pk, comment_pk):
    posting = get_object_or_404(Posting, pk=posting_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.user != comment.author:
        return redirect('discussion:posting_detail') 

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            return redirect('discussion:posting_detail', posting.pk)

    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'discussion/form.html', {  # html 추후 변경
        'form':form,
    })

@login_required
@require_POST
def comment_delete(request, posting_pk, comment_pk):
    posting = get_object_or_404(Posting, pk=posting_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.user == comment.author:
       comment.delete()

    return redirect('discussion:posting_detail', posting.pk)

@login_required
@require_POST
def comment_agree(request, posting_pk, comment_pk):
    user = request.user
    posting = get_object_or_404(Posting, pk=posting_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    if comment.users_agree.filter(pk=user.pk).exists(): 
        comment.users_agree.remove(user)
    
    else:
        comment.users_agree.add(user)

    return redirect('discussion:posting_detail', posting.pk)  

@login_required
@require_POST
def comment_disagree(request, posting_pk, comment_pk):
    user = request.user
    posting = get_object_or_404(Posting, pk=posting_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    if comment.users_disagree.filter(pk=user.pk).exists():
        comment.users_disagree.remove(user)

    else:
        comment.users_disagree.add(user)

    return redirect('discussion:posting_detail', posting.pk)  

@login_required
@require_POST
def reply_create(request, posting_pk, comment_pk):
    posting = get_object_or_404(Posting, pk=posting_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    form = ReplyForm(request.POST)
    if form.is_valid():
        reply = form.save(commit=False)
        reply.comment = comment
        reply.author = request.user
        reply.save()
        return redirect('discussion:posting_detail', posting.pk)
    else:
        return HttpResponseBadRequest('Can not proceed.')

@login_required
@require_http_methods(['GET', 'POST'])
def reply_update(request, posting_pk, reply_pk):
    posting = get_object_or_404(Posting, pk=posting_pk)
    reply = get_object_or_404(Reply, pk=reply_pk)

    if request.user != reply.author:
        return redirect('discussion:posting_detail') 

    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=reply)
        if form.is_valid():
            reply = form.save()
            return redirect('discussion:posting_detail', posting.pk)

    else:
        form = ReplyForm(instance=reply)
    
    return render(request, 'discussion/form.html', {  # html 추후 변경
        'form':form,
    })

@login_required
@require_POST
def reply_delete(request, posting_pk, reply_pk):
    posting = get_object_or_404(Posting, pk=posting_pk)
    reply = get_object_or_404(Reply, pk=reply_pk)


    if request.user == reply.author:
       reply.delete()

    return redirect('discussion:posting_detail', posting.pk)
