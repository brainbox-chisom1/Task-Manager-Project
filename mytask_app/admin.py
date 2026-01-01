from django.contrib import admin
from .models import Task, Tag, Remainder
#Register your models here.

admin.site.register(Task)
admin.site.register(Tag)
admin.site.register(Remainder)

# class TaskAdmin(admin.ModelAdmin):
#     """customize the admin homepage"""
#     list_display = ['title', 'date', 'priority']
 
# class ListAdmin(admin.ModelAdmin):
#     """customize the display of the ToDO List items"""
#     list_display = ['name', 'tag', 'date_added']

# class TagAdmin(admin.ModelAdmin):
#     """customized list of Tags"""
#     list_display = ['tag']

# # admin.site.register(Task,TaskAdmin)
# admin.site.register(Tag, TagAdmin)
# admin.site.register(List, ListAdmin)
# admin.site.site_header = 'ToDo-List'
# admin.site.site_title = 'My ToDo-List'