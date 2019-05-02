from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from mySite.models import Attachment, Comment


# Create your views here.


# def home(request):
#     return render(request, 'mySite\home.html')
index = 0


class HomeView(View):

    def get(self, request):
        global index
        index = 0
        attachments = Attachment.objects.all()[0:5]
        return render(request, 'mySite/home.html', context={'attachments': attachments})


class AttachmentDetail(View):

    def get(self, request, numb):
        attachment = get_object_or_404(Attachment, id=numb)
        comments = attachment.comment.all()
        # comments = Comment.objects.filter(attachment=attachment)
        return render(request, 'mySite/attachment.html', context={'attachment': attachment,
                                                                  'comments': comments})


def pagination(request):
    data = Attachment.objects.all()
    global index

    if request.GET.get('identifier') == 'next':
        index = index + 5
    elif request.GET.get('identifier') == 'previous':
        index = index - 5

    if index > 5:
        prev = True
    else:
        prev = False
    if len(data) > index:
        nxt = True
    else:
        nxt = False
    data2 = []
    for i in data[index - 5: index]:
        data2.append({'owner': str(i.owner),
                      'name': i.__str__(),
                      'date': i.date.strftime("%d %B %Y %I:%M"),
                      'id': i.id,
                      'nxt': nxt,
                      'prev': prev})
    context = {'elements': data2}
    return JsonResponse(context)
