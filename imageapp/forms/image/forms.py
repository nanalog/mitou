from django import forms
from imageapp.models import ImageData


class ImageForm(forms.ModelForm):

    class Meta:
        model = ImageData
        fields = ['title', 'image']
