from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin  # これを追加

from imageapp.models import ImageData
from imageapp.forms.image.forms import ImageForm
from imageapp.ai.model_loader import predict

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

import os

# ユーザー登録用のクラスを追加
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login') # 登録後はログイン画面へ飛ばす
    template_name = 'registration/signup.html'


# すべてのクラスに LoginRequiredMixin を継承させます
class ImageListView(LoginRequiredMixin, generic.ListView):
    model = ImageData
    queryset = ImageData.objects.order_by('-created_at')
    template_name = 'imageapp/image_list.html'

class ImageCreateView(LoginRequiredMixin, generic.CreateView):
    model = ImageData
    form_class = ImageForm
    template_name = 'imageapp/image_form.html'
    success_url = reverse_lazy('imageapp:list_image')

    def form_valid(self, form):
        # 現在ログイン中のユーザーをモデルに紐付けることも可能です（推奨）
        # obj = form.save(commit=False)
        # obj.user = self.request.user
        # obj.save()
        
        obj = form.save()
        image_path = obj.image.path
        result, prob = predict(image_path)
        obj.prediction = result
        obj.probability = prob * 100
        obj.save()
        return redirect('imageapp:list_image')

class ImageDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ImageData
    success_url = reverse_lazy('imageapp:list_image')

    def get(self, request, *args, **kwargs):
        # getメソッドでの削除実装もLoginRequiredMixinで保護されます
        obj = ImageData.objects.get(pk=kwargs['pk'])
        if obj.image:
            if os.path.isfile(obj.image.path):
                os.remove(obj.image.path)
        obj.delete()
        return redirect('imageapp:list_image')
