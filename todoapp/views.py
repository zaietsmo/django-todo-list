from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Tag


def home(request):
    tasks = Task.objects.order_by('is_done', '-created_at')
    return render(request, 'todoapp/home.html', {'tasks': tasks})


def task_create(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        deadline = request.POST.get('deadline')
        if deadline:
            deadline = deadline
        else:
            deadline = None

        task = Task.objects.create(
            content=content,
            deadline=deadline
        )

        tags = request.POST.getlist('tags')
        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            task.tags.add(tag)

        return redirect('home')

    tags = Tag.objects.all()
    return render(request, 'todoapp/task_form.html', {'tags': tags})


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        deadline = request.POST.get('deadline')
        if deadline:
            deadline = deadline
        else:
            deadline = None

        task.content = content
        task.deadline = deadline
        task.save()

        task.tags.clear()
        tags = request.POST.getlist('tags')
        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            task.tags.add(tag)

        return redirect('home')

    tags = Tag.objects.all()
    return render(request, 'todoapp/task_form.html', {'task': task, 'tags': tags})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('home')
    return render(request, 'todoapp/task_confirm_delete.html', {'task': task})


def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_done = not task.is_done
    task.save()
    return redirect('home')


def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'todoapp/tag_list.html', {'tags': tags})


def tag_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        tag = Tag.objects.create(name=name)
        return redirect('tag_list')
    return render(request, 'todoapp/tag_form.html')


def tag_update(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        tag.name = request.POST['name']
        tag.save()
        return redirect('tag_list')
    return render(request, 'todoapp/tag_form.html', {'tag': tag})


def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        tag.delete()
        return redirect('tag_list')
    return render(request, 'todoapp/tag_confirm_delete.html', {'tag': tag})
