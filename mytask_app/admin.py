from django.contrib import admin
from .models import Task, Tag, Remainder
#Register your models here.



class TaskAdmin(admin.ModelAdmin):
    """customize the admin homepage"""
    list_display = ['task_name', 'date_added', 'piority_level', 'tag']
    list_filter = ['tag']
 


class TagAdmin(admin.ModelAdmin):
    """customized list of Tags"""
    list_display = ['tag_name', 'owner']#see who created each tags

class RemainderAdmin(admin.ModelAdmin):
    """show details of upcoming tasks"""
    list_display = ['task_name', 'date', 'owner']
    

admin.site.register(Task, TaskAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Remainder, RemainderAdmin)
admin.site.site_header = 'Precious Task Manager'
admin.site.site_title = 'Task Management Dashboard'