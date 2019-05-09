from django.db.models import Q
from django.http import JsonResponse, Http404
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from mySite import forms
from mySite.models import Attachment, Comment
from audioShuffler import audio_shuffler
from os import path



# Create your views here.


index = None


class HomeView(TemplateView):
    form_for_attachment = forms.AttachmentForm
    data = None

    def get(self, request, *args, **kwargs):
        global index
        global data
        index = 0
        search = request.GET.get('search', '')

        if search:
            data = Attachment.objects.filter(Q(file__icontains=search) | Q(name__icontains=search))
        else:
            data = Attachment.objects.all().order_by('-date')

        context = {'form_for_attachment': self.form_for_attachment}
        return render(request, 'mySite/home.html', context)

    def post(self, request):
        global index
        index = 0
        form = forms.AttachmentForm(request.POST, request.FILES)

        context = {'form_for_attachment': form}

        form.instance.owner = self.request.user

        if form.is_valid():
            form.save()
            return render(request, 'mySite/home.html', context)
        else:
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

        if 'SendComment' in request.POST:
            form = forms.CommentForm(request.POST)
            comments = attachment.comment.all()
            context = {'attachment': attachment,
                       'comments': comments,
                       'form_for_comment': form}

            form.instance.owner = self.request.user
            form.instance.attachment = attachment

            if form.is_valid():
                form.save()
                return render(request, 'mySite/attachment.html', context)
            else:
                return render(request, 'mySite/attachment.html', context)
        elif 'Shuffled' in request.POST:
            form = forms.ShufflerForm(request.POST)

            # file_path = path.abspath(str(attachment.file))
            file_path = path.abspath(path.join((path.dirname(path.dirname(path.abspath(str(attachment.file))))), 'media', str(attachment.file)))
            file_type = path.splitext(path.basename(str(attachment.file)))[-1]
            shuffle_flag = form['shuffle_flag'].value()
            number_of_slices = int(form['number_of_slices'].value())
            percentage = int(form['percentage'].value())
            times = int(form['times'].value())

            print('W2WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW')
            print(file_path)

            shuffled_file = audio_shuffler.slice_n_dice(file_path, file_type,
                                                        shuffle_flag, number_of_slices,
                                                        percentage, times)
        else:
            raise Http404


def pagination(request):
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
