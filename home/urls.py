from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('about-me/', views.aboutMe, name='aboutMe'),
    path('home/tag/<slug:tag_slug>/', views.all_tags_list, name='all_tags_list'),
    path('publications/', views.publications, name='publications'),  
    path('publications/tag/<slug:tag_slug>/', views.publications_tags_list, name='publications_tags_list'),
    path('projects/', views.projects, name='projects'),
    path('projects/tag/<slug:tag_slug>/', views.projects_tags_list, name='projects_tags_list'),
    path('post/<slug:slug>', views.post_detail, name='post_detail'),
]
