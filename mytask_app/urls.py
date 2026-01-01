from django.urls import path
from . import views

urlpatterns = [
    path('login_user', views.login_user, name='login_user'),
    path('register_user', views.register_user, name='register_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('', views.index, name='index'),
    path('new_tag/', views.new_tag, name='new_tag'),
    path('add_task/', views.add_task, name='add_task'),
    path('delete_task/<int:id>/', views.delete_task, name='delete_task'),
    path('delete_tag/<int:id>/', views.delete_tag, name='delete_tag'),
    path('update_tag/<int:id>/', views.update_tag, name='update_tag'),
    path('remainder/<int:id>/', views.remainder, name='set_remainder'),
    path('task/<int:id>/', views.view_task, name='view_task'),
    path('upcoming_task', views.upcoming_task, name='upcoming_task'),
    path('completed_task', views.completed_task, name='completed_task'),
    
]