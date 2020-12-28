from django.urls import path
from . import views

app_name = 'actioncam'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:upload_video_id>/', views.detail, name='detail'),
    path('new/', views.video_new, name='new'),
]