# Generated by Django 3.1.4 on 2020-12-29 05:53

import actioncam.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actioncam', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload_video',
            name='create_date',
            field=models.DateTimeField(verbose_name=actioncam.models.get_file_name),
        ),
    ]
