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
from .models import Tag, Task, Remainder, Completed_task
from . import forms


#authenticate every users data and validate credentials to login
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

#Using django model for User to create account
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


#logOut function from existing user
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect("/login_user")
    return render(request, 'confirm_logout.html')


#homepage and search functions by Tag associated with task
@login_required(login_url='login_user')
def index(request):
    """the homepage and the search functionality"""
    #filtering by owners data
    task = Task.objects.filter(owner=request.user)
    form = forms.SearchTag(request.POST or None, user=request.user)#passed user to the form so the tag form could be validated by a users data
   
    if request.method == 'POST' and form.is_valid():
        product_tag = form.cleaned_data.get('tag')# get the tag from the form submitted
       
        if product_tag:
            task = task.filter(tag=product_tag, owner=request.user)

    return render(request, 'index.html', {'task': task, 'form': form})

#Delete tasks that are not needed or completed
@login_required(login_url='login_user')
def delete_task(request, id):
    """delete a task"""
    task = get_object_or_404(Task, id=id)
    if request.method == "POST":
        task.delete()
        return redirect('/')
    else:
        return render(request, 'confirm_delete.html')


#displays new tags created by each user where each user owns his/her own data
@login_required(login_url='login_user')
def new_tag(request):
    """create tags"""
    tag = Tag.objects.filter(owner=request.user)#filter by user to get the tag create by that user
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


#Delete tag and the tasks associated by that tag
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


#get the existing tag and allow editing and update to a new tag name
@login_required(login_url='login_user')
def update_tag(request, id):
    """update an existing tag"""
    tag = get_object_or_404(Tag, id=id, owner=request.user)
    form = forms.TagForm(instance=tag)#gets the tag instance to be updated
    if request.method == "POST":
        #note the instance coming from the frontend to be updated by the new passed argument must be added in the form below
        form = forms.TagForm(request.POST, instance=tag)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user#bind to the user attribute
            task.save()
            return redirect('new_tag')
    return render(request, 'update_tag.html', {'tag': tag, 'form': form})


#function renders a form for adding tasks to the task model
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


#keeps track of all tasks that was set go off at a particular time
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




#allows viewing of create task details like descriptions, tags, piority-level but can't edit or change details there
@login_required(login_url='login_user')
def view_task(request, id):
    """view each task description"""
    task = Task.objects.get(id=id)
    return render(request, 'tasks.html', {'task': task, })


#shows the list of tasks that has a time stamp around them
@login_required(login_url='login_user')
def upcoming_task(request):
    """show all the upcoming task based on the remainder operation set"""
    task_reminder = Remainder.objects.filter(owner=request.user)  
    return render(request, 'upcoming_task.html', {'task': task_reminder})


#Show the list of all completed tasks
@login_required(login_url='login_user')
def complete_task(request, id):
    """get the task properties and ask if completed."""
    task = get_object_or_404(Task, id=id)

    if request.method == "POST":
        Completed_task.objects.create(
            task=task.task_name,
            tag_name=task.tag,
            description=task.description,
            owner=request.user
        )
        task.delete()
        return redirect('done_task')

    return render(request, 'new_complete.html', {'task': task})

def all_completed_task(request):
    """list all tasks that are completed"""
    task = Completed_task.objects.filter(owner=request.user)
    return render(request, 'done_task.html', {'task': task})




# def send_mail(to_email, task_name):
#     task = Task.objects.all()
#     subject = "Your Upcoming Task"
#     message = f"Reminder: You have a pending task - {task.task_name}"
#     from_email = settings.EMAIL_HOST_USER

#     send_mail(
#         subject,
#         message,
#         from_email,
#         [to_email],
#         fail_silently=False
#     )

# def is_ten_minutes_to_due(task):
#     due_datetime = datetime.combine(
#         task.date,
#         task.time
#     )

#     due_datetime = timezone.make_aware(due_datetime)
#     now = timezone.now()

#     time_left = due_datetime - now

#     return timedelta(minutes=9, seconds=50) <= time_left <= timedelta(minutes=10, seconds=10)
