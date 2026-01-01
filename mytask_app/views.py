from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import Tag, Task, Remainder
from . import forms


def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
 
        if user is not None:#if True
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request, f"Invalid Username or password")
    return render(request, 'login_user.html')

def register_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = forms.RegisterForm()
    if request.method == "POST":
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login_user')
    return render(request, 'register_page.html', {'form': form})

def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect("/login_user")
    return render(request, 'confirm_logout.html')

@login_required(login_url='login_user')
def index(request):
    """the homepage and the search functionality"""
    task = Task.objects.filter(owner=request.user)
    form = forms.SearchTag(request.POST or None, user=request.user)
   
    if request.method == 'POST' and form.is_valid():
        product_tag = form.cleaned_data.get('tag')# get the tag from the form submitted
       
        if product_tag:
            task = task.filter(tag=product_tag, owner=request.user)

    return render(request, 'index.html', {'task': task, 'form': form})

@login_required(login_url='login_user')
def delete_task(request, id):
    """delete a task"""
    task = get_object_or_404(Task, id=id)
    if request.method == "POST":
        task.delete()
        return redirect('/')
    else:
        return render(request, 'confirm_delete.html')

# class Tag(object):
    # """class based view"""
    # def __init__(self, form):
    #     self.form = forms.TagForm()

@login_required(login_url='login_user')
def new_tag(request):
    """create tags"""
    tag = Tag.objects.filter(owner=request.user)
    if request.method == "POST":
        form = forms.TagForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()

            return redirect('new_tag')
    else:
        form = forms.TagForm()
    return render(request, 'new_tag.html', {'form': form, 'tag': tag})

@login_required(login_url='login_user')
def delete_tag(request, id):
    """delete tag based on id"""
    tag = Tag.objects.get(id=id) #returns tag.id'
    task = tag.tasks.all()# gets all the tasks associated with the Tag
    if request.method == "POST":
        tag.delete()
        return redirect('/new_tag')
    else:
        return render(request, 'confirm_tag.html', {'tag': tag, 'task': task,})


@login_required(login_url='login_user')
def update_tag(request, id):
    """update an existing tag"""
    tag = get_object_or_404(Tag, id=id, owner=request.user)
    form = forms.TagForm(instance=tag)#(tech)
    if request.method == "POST":
        form = forms.TagForm(request.POST, instance=tag)#note the instance coming from the frontend to be updated by the new passed argument
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return redirect('new_tag')
    return render(request, 'update_tag.html', {'tag': tag, 'form': form})


@login_required(login_url='login_user')
def add_task(request):
    """new task"""
    form = forms.AddTask(user=request.user)
    if request.method == 'POST':
        form = forms.AddTask(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user #assign each task to a particular user
            task.save()

            return redirect('/')
    return render(request, 'add_task.html', {'form': form})

@login_required(login_url='login_user')
def remainder(request, id):
    """set a remainder for a particular task"""
    task = Task.objects.get(id=id)
    form = forms.RemainderForm(instance=task, user=request.user)

    if request.method == "POST":
        form = forms.RemainderForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return redirect("/upcoming_task")

    return render(request, 'remainder.html', {'task': task, 'form': form})


def send_mail(to_email, task_name):
    task = Task.objects.all()
    subject = "Your Upcoming Task"
    message = f"Reminder: You have a pending task - {task.task_name}"
    from_email = settings.EMAIL_HOST_USER

    send_mail(
        subject,
        message,
        from_email,
        [to_email],
        fail_silently=False
    )

def remainder_mail(request):
    """check the remainder table and send mail to tasks closer to 10mins or in 10mins range"""
    #steps
    #query the remainder table to get the objects
    #get the time and date 
    #combine both time stamps
    #get the current time
    #subtract the remainder time stamp from the current time
    #check if the time is equals to 10mins and send a mail
    remainder = Remainder.objects.all()
    time = remainder.time
    date = remainder.date
    pass


@login_required(login_url='login_user')
def view_task(request, id):
    """view each task description"""
    task = Task.objects.get(id=id)
    return render(request, 'tasks.html', {'task': task, })

@login_required(login_url='login_user')
def upcoming_task(request):
    """show all the upcoming task based on the remainder operation set"""
    task_reminder = Remainder.objects.filter(owner=request.user)  
    return render(request, 'upcoming_task.html', {'task': task_reminder})


@login_required(login_url='login_user')
def completed_task(request):
    """show all the list of tasks that are completed"""
    task = Task.objects.all()
    request.completed = 1

    if request.completed == 1:
        task = Task.objects.filter(completed=1).values()
        
    return render(request, 'task_complete.html', {'task': task})