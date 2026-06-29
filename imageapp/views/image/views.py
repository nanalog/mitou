from django.views import generic
from django.urls import reverse_lazy

from imageapp.models import ImageData
from imageapp.forms.image.forms import ImageForm
from django.shortcuts import redirect

from imageapp.ai.model_loader import predict
import os
class ImageListView(generic.ListView):

    model = ImageData

    queryset = ImageData.objects.order_by('-created_at')

    template_name = 'imageapp/image_list.html'


class ImageCreateView(generic.CreateView):

    model = ImageData

    form_class = ImageForm

    template_name = 'imageapp/image_form.html'

    success_url = reverse_lazy('imageapp:list_image')

    def form_valid(self, form):

        obj = form.save()

        image_path = obj.image.path

        result, prob = predict(image_path)

        obj.prediction = result

        obj.probability = prob * 100

        obj.save()

        return redirect('imageapp:list_image')

class ImageDeleteView(generic.DeleteView):

    model = ImageData

    success_url = reverse_lazy('imageapp:list_image')

    def get(self, request, *args, **kwargs):

        obj = ImageData.objects.get(pk=kwargs['pk'])
        
        if obj.image:
           if os.path.isfile(obj.image.path):
              os.remove(obj.image.path)
        obj.delete()

        return redirect('imageapp:list_image')
