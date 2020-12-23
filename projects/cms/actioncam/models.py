from django.db import models

def get_file_name(instance, filename):
    ext = filename.split('_')
    return (ext[0][:2]+ext[1][:2]+ext[1][2:])   # 파일명에 기록된 날짜기준
# 2020_1222_145701_003

def get_file_date(instance, filename):
    ext = filename.split('_')
    return '.'.join(ext[0][:2],'-',ext[1][:2],'-',ext[1][2:])

class Upload_video(models.Model):
    subject = models.CharField(max_length=200)   # 파일명으로부터 수정필요
    pub_date = models.DateTimeField()
    description = models.TextField()
    file = models.FileField()
    create_date = models.CharField(max_length=20)  # 파일명으로부터 수정필요
    emergency = models.BooleanField(null=True)

