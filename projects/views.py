from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Project
from .forms import ProjectForm

def project_list(request):
    # Достаем из базы все проекты и сортируем от новых к старым 
    projects = Project.objects.all().order_by('-created_at')
    
    # Отдаем htm;l шаблон и передаем в него список проектов
    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            # Сохраняем, но пока не отправляем в базу
            project = form.save(commit=False)
            # Автором назначаем текущего залогиненного пользователя
            project.owner = request.user
            project.save()
            # Добавляем автора в список участников
            project.participants.add(request.user)
            
            # Перенаправляем на страницу созданного проекта
            return redirect('projects:project_details', pk=project.pk)
    else:
        form = ProjectForm()
        
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})

def project_details(request, pk):
    # Ищем проект по id, если не найдем - выдаст 404 ошибку
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project-details.html', {'project': project})

@login_required
@require_POST
def complete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    # Проверяем, что нажал fdnjh и проект еще открыт
    if project.owner == request.user and project.status == 'open':
        project.status = 'closed'
        project.save()
        return JsonResponse({"status": "ok", "project_status": "closed"})
    return JsonResponse({"status": "error"}, status=403)

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        # Передаем существующий проект в форму, чтобы обновить его, а не создать новый
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:project_details', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    
    # is_edit=True меняет текст кнопки с опубликовать на сохранить
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True})

@login_required
def favorite_projects(request):
    # Достаем только те проекты, которые пользователь добавил в избранное
    projects = request.user.favorites.all().order_by('-created_at')
    return render(request, 'projects/favorite_projects.html', {'projects': projects})

@login_required
@require_POST
def toggle_participate(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user in project.participants.all():
        project.participants.remove(request.user)
        is_participant = False
    else:
        project.participants.add(request.user)
        is_participant = True
    return JsonResponse({"status": "ok", "participant": is_participant})

@login_required
@require_POST
def toggle_favorite(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project in request.user.favorites.all():
        request.user.favorites.remove(project)
        favorited = False
    else:
        request.user.favorites.add(project)
        favorited = True
    return JsonResponse({"status": "ok", "favorited": favorited})
