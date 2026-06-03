from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from team_finder.services import get_paginated_page
from .forms import ProjectForm
from .models import Project


def project_list(request):
    # Достаем из базы все проекты и сортируем от новых к старым 
    projects = Project.objects.select_related('owner').prefetch_related('participants').order_by('-created_at')
    
    # Отдаем htm;l шаблон и передаем в него список проектов
    page_obj = get_paginated_page(request, projects)
    return render(request, 'projects/project_list.html', {'projects': page_obj})

@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)
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
    if project.owner == request.user and project.status == Project.STATUS_OPEN:
        project.status = Project.STATUS_CLOSED
        project.save()
        return JsonResponse({"status": "ok", "project_status": "closed"})
    return JsonResponse({"status": "error"}, status=HTTPStatus.FORBIDDEN)

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
        # Передаем существующий проект в форму, чтобы обновить его, а не создать новый
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('projects:project_details', pk=project.pk)
    # is_edit=True меняет текст кнопки с опубликовать на сохранить
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True})

@login_required
def favorite_projects(request):
    # Достаем только те проекты, которые пользователь добавил в избранное
    projects = request.user.favorites.select_related('owner').prefetch_related('participants').order_by('-created_at')
    page_obj = get_paginated_page(request, projects)
    return render(request, 'projects/favorite_projects.html', {'projects': page_obj})

@login_required
@require_POST
def toggle_participate(request, pk):
    project = get_object_or_404(Project, pk=pk)
    is_participant = False
    if project.participants.filter(id=request.user.id).exists():
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)
        is_participant = True
    return JsonResponse({"status": "ok", "participant": is_participant})

@login_required
@require_POST
def toggle_favorite(request, pk):
    project = get_object_or_404(Project, pk=pk)
    favorited = False
    if request.user.favorites.filter(id=project.id).exists():
        request.user.favorites.remove(project)
    else:
        request.user.favorites.add(project)
        favorited = True
    return JsonResponse({"status": "ok", "favorited": favorited})
