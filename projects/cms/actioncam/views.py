from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("안녕하세요! ActionCam 관리시스템에 오신것을 환영합니다")