from django.urls import path
from imageapp.views.image.views import (
    ImageListView,
    ImageCreateView,
    ImageDeleteView,
)

app_name = 'imageapp'

urlpatterns = [
    path('images/', ImageListView.as_view(), name='list_image'),
    path('images_new/', ImageCreateView.as_view(), name='create_image'),
    path('images_delete/<int:pk>/',ImageDeleteView.as_view(),name='delete_image'),
]
