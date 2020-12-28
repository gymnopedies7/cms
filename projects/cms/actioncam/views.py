from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Upload_video
from django.urls import reverse
from django.utils import timezone

def index(request):
    
    video_list = Upload_video.objects.order_by('-create_date')
    context = {'video_list':video_list}

    return render(request, 'actioncam/video_list.html',context)

def detail(request, upload_video_id):
    
    video = Upload_video.objects.get(id=upload_video_id)
    context = {'video':video}

    return render(request, 'actioncam/video_detail.html',context)

# Ref : djangogirls djangotube
def video_new(request):
    if request.method == 'POST':
        title = request.POST['title']
        Upload_video.objects.create(title=title, description=description)
        return redirect(reverse('actioncam:index'))
    elif request.method == 'GET':
        return render(request, 'actioncam/video_new.html')