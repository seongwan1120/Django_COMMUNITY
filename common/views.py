from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest

from .forms import CustomUserCreationForm

# Create your views here.

User = get_user_model()

@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('discussion:posting_index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('discussion:posting_index')
        
    else:
        form = CustomUserCreationForm()
    return render(request, 'common/signup.html',{
        'form':form,
    })

@require_http_methods(['GET', 'POST'])
def signin(request):
    if request.user.is_authenticated:
        return redirect('discussion:posting_index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.GET.get('next') or 'discussion:posting_index')
    
    else:
        form = AuthenticationForm()
    return render(request, 'common/signin.html',{
        'form': form,
    })

def signout(request):
    logout(request)
    return redirect('discussion:posting_index')

@require_safe
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_following = request.user.followings.filter(pk=profile_user.pk).exists()

    return render(request, 'common/profile.html',{
        'profile_user':profile_user,
        'is_following':is_following,
    })

@login_required
@require_POST
def follow(request, username):
    one = request.user
    the_other = get_object_or_404(User, username=username)
    
    if one == the_other:
        return HttpResponseBadRequest('Following yourself is forbidden.')

    if one.followings.filter(pk=the_other.pk).exists(): 
        one.followings.remove(the_other)
    else: 
        one.followings.add(the_other)
    return redirect('common:profile', the_other.username)