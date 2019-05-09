from django import forms
from .models import Attachment, Comment


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file', 'name']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={'cols': 30, 'rows': 2}),
        }


class ShufflerForm(forms.Form):
    number_of_slices = forms.IntegerField(min_value=0, label='Number of slices')
    percentage = forms.IntegerField(min_value=0, max_value=100, label='Сhance to reverse (0 - 100)%')
    times = forms.IntegerField(min_value=1, label='Number of repeats')
    shuffle_flag = forms.BooleanField(required=False, label='Shuffle the result?')
