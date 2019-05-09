from os import path
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core.validators import FileExtensionValidator


# Create your models here.


def get_upload_to_path(instance, filename):
    return '{0}/{1}'.format(type(instance).__name__, filename)


class Attachment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(null=False,
                            upload_to=get_upload_to_path,
                            validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav'])])
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        if self.name == '':
            return path.splitext(path.basename(str(self.file)))[0]
        return self.name


class Comment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(null=False)
    attachment = models.ForeignKey(Attachment, related_name="comment", on_delete=models.CASCADE)
