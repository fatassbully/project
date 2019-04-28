from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from mySite.models import Attachment, Comment


# Create your views here.


# def home(request):
#     return render(request, 'mySite\home.html')


class HomeView(View):

    def get(self, request):
        attachments = Attachment.objects.all()[0:3]
        return render(request, 'mySite/home.html', context={'attachments': attachments})


class AttachmentDetail(View):

    def get(self, request, numb):
        attachment = get_object_or_404(Attachment, id=numb)
        comments = attachment.comment.all()
        # comments = Comment.objects.filter(attachment=attachment)
        return render(request, 'mySite/attachment.html', context={'attachment': attachment,
                                                                  'comments': comments})
