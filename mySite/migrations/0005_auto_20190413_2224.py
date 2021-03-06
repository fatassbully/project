# Generated by Django 2.1.7 on 2019-04-13 19:24

import django.core.validators
from django.db import migrations, models
import mySite.models


class Migration(migrations.Migration):

    dependencies = [
        ('mySite', '0004_auto_20190331_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='file',
            field=models.FileField(upload_to=mySite.models.get_upload_to_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp3', 'wav'])]),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='name',
            field=models.CharField(default=models.FileField(upload_to=mySite.models.get_upload_to_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp3', 'wav'])]), max_length=100),
        ),
    ]
