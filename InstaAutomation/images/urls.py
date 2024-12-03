from django.urls import path
from . import views

urlpatterns = [
    path('', views.ImagesView.as_view(), name='image-home'),
]