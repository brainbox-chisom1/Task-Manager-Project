from django.db import models
from django.contrib.auth.models  import User
# Create your models here.

#this is the category section for each tasks
class Tag(models.Model):
    """Holds the category of each task created"""
    tag_name = models.CharField(max_length=50, null=False, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag_name


#created only for registerations of tasks and keeping users entry
class Task(models.Model):
    """Task properties are created here"""
    importance = {
        'High': 'High',
        'Medium': 'Medium',
        'Low': 'Low',
    }
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tasks')
    task_name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(max_length=1000, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    piority_level = models.CharField(max_length=6, choices=importance.items(), null=False)
    completed = models.IntegerField(default=0)#renders on the home page the completed 
    completed_date = models.DateTimeField(auto_now=True)
    upcoming_task = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    remainder_sent = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.task_name}, {self.description[:12]}..."


#Extracts tasks from Task Model and keeps record of user's tasks and send a mail once time is close to due
class Remainder(models.Model):
    """Keeps record of the upcoming tasks and sends a notification to the email"""
    #if stop_time is close:
    task_name = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(null=False, blank=True)
    time = models.TimeField(null=False, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    remainder_sent = models.BooleanField(default=False)

    def __str__(self):
        return f'task name {self.task_name}, Stop Date: {self.date}, Stop Time: {self.time}'
    


#stores all completed tasks with their time and date of completed inpressions    
class Completed_task(models.Model):
    """complete tasks are create with the time and date of completion"""
    task = models.CharField(max_length=50, null=True, blank=True)
    tag_name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    time = models.TimeField(auto_now_add=True, null=True, blank=False)
    date = models.DateField(auto_now_add=True, null=True, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Completed task {self.task} and date {self.date}'

    















# class Tag(models.Model):
#     tag = models.CharField(max_length=50, null=False)#for searching for a particular task

#     def __str__(self):
#         return f'{self.tag}'


# class List(models.Model):
#     """The list table model holding all the events or tasks created and linking each to a specific tag"""
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="tasks")
#     name = models.CharField(max_length=50, null=False, blank=False)
#     description = models.TextField(null=True, blank=True)
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.name}'


# class Task(models.Model):
#     choice = (
#         ('High', 'High'),
#         ('Medium', 'Medium'),
#         ('Low', 'Low'),
#     )
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
#     title = models.CharField(max_length=50, null=False)#name of the task
#     description = models.TextField(null=True, blank=True)
#     due_date = models.DateField()#the date that the reminder will go off
#     date = models.DateTimeField(auto_now_add=True)
#     priority = models.CharField(max_length=50, null=False, choices=choice)#three levels of priority
#     reminder = models.DateField()
#     recur = models.BooleanField(default=False)
#     checkbox = models.BooleanField(default=False)

#     def __str__(self):
        #return f'{self.title}'

