from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import RegisterForm, LoginForm, ProfileEditForm, ChangePasswordForm
from .models import User

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Сразу авторизуем после регистрации
            return redirect('/projects/list/')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            return redirect('/projects/list/')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/projects/list/')

def user_list(request):
    users = User.objects.all().order_by('id')
    active_filter = request.GET.get('filter')

    if active_filter and request.user.is_authenticated:
        if active_filter == "Авторы избранных проектов":
            owners = request.user.favorites.values_list('owner', flat=True)
            users = users.filter(id__in=owners)
        elif active_filter == "Авторы проектов, в которых я участвую":
            owners = request.user.participated_projects.values_list('owner', flat=True)
            users = users.filter(id__in=owners)
        elif active_filter == "Пользователи, которым нравятся мои проекты":
            users = users.filter(favorites__in=request.user.owned_projects.all()).distinct()
        elif active_filter == "Участники моих проектов":
            users = users.filter(participated_projects__in=request.user.owned_projects.all()).distinct()

    # Пагинация (12 профилей на страницу)
    paginator = Paginator(users, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/participants.html', {
        'participants': page_obj, 
        'active_filter': active_filter
    })

def user_details(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    return render(request, 'users/user-details.html', {'user': user_obj})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:user_details', pk=request.user.pk)
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_password1'])
            request.user.save()
            # Обновляем сессию, чтоб пользователя не выкинуло из аккаунта после смены пароля
            update_session_auth_hash(request, request.user)
            return redirect('users:user_details', pk=request.user.pk)
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})
