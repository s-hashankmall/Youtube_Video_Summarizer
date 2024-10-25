from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_videos, name='search_videos'),
    path('summary/<str:video_id>/', views.summarize_video, name='summarize_video'), 
    path('qna/<str:video_id>/', views.qna, name='qna'),
]
