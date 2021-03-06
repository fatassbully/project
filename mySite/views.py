from django.db.models import Q
from django.http import JsonResponse, Http404
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from mySite import forms
from mySite.models import Attachment
from audioShuffler import audio_shuffler
from os import path
from project import settings

# Create your views here.


index = 0
data = None


class HomeView(TemplateView):
    form_for_attachment = forms.AttachmentForm

    def get(self, request, *args, **kwargs):
        global index
        global data
        index = 0
        search = request.GET.get('search', '')

        if search:
            data = Attachment.objects.filter(Q(name__exact='') &
                                             Q(file__iregex="Attachment/.*" + search + ".*") |
                                             Q(name__icontains=search)).order_by('-date')
        else:
            data = Attachment.objects.all().order_by('-date')

        context = {'form_for_attachment': self.form_for_attachment}
        return render(request, 'mySite/home.html', context)

    def post(self, request):
        global index
        global data
        index = 0
        form = forms.AttachmentForm(request.POST, request.FILES)

        context = {'form_for_attachment': self.form_for_attachment}

        form.instance.owner = self.request.user

        if form.is_valid():
            form.save()

        data = Attachment.objects.all().order_by('-date')
        return render(request, 'mySite/home.html', context)


class AttachmentDetail(TemplateView):
    form_for_comment = forms.CommentForm
    form_for_shuffler = forms.ShufflerForm

    def get(self, request, *args, **kwargs):
        attachment = get_object_or_404(Attachment, id=kwargs['numb'])
        comments = attachment.comment.all()
        context = {'attachment': attachment,
                   'comments': comments,
                   'form_for_comment': self.form_for_comment,
                   'form_for_shuffler': self.form_for_shuffler}
        return render(request, 'mySite/attachment.html', context)

    def post(self, request, *args, **kwargs):
        attachment = get_object_or_404(Attachment, id=kwargs['numb'])
        comments = attachment.comment.all()

        if 'SendComment' in request.POST:
            form = forms.CommentForm(request.POST)
            context = {'attachment': attachment,
                       'comments': comments,
                       'form_for_comment': self.form_for_comment,
                       'form_for_shuffler': self.form_for_shuffler}

            form.instance.owner = self.request.user
            form.instance.attachment = attachment

            if form.is_valid():
                form.save()

            return render(request, 'mySite/attachment.html', context)
        elif 'Shuffled' in request.POST:
            form = forms.ShufflerForm(request.POST)

            file_path = path.join(settings.BASE_DIR, 'media',
                                  str(attachment.file))
            shuffle_flag = form['shuffle_flag'].value()
            number_of_slices = int(form['number_of_slices'].value())
            percentage = int(form['percentage'].value())
            times = int(form['times'].value())

            shuffled_file = audio_shuffler.slice_n_dice(file_path, shuffle_flag, number_of_slices,
                                                        percentage, times)

            context = {'attachment': attachment,
                       'comments': comments,
                       'form_for_comment': self.form_for_comment,
                       'form_for_shuffler': form,
                       'shuffled_file': shuffled_file}
            return render(request, 'mySite/attachment.html', context)
        else:
            raise Http404


def pagination(request):
    global index
    data2 = []

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

    for i in data[index - 5: index]:
        data2.append({'owner': str(i.owner),
                      'name': i.__str__(),
                      'date': i.date.strftime("%d %B %Y %I:%M"),
                      'id': i.id,
                      'nxt': nxt,
                      'prev': prev})
    context = {'elements': data2}
    return JsonResponse(context)
