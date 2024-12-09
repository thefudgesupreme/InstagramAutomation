from django.urls import path
from . import views

urlpatterns = [
    path('', views.ImagesView.as_view(), name='images-home'),
    path('create', views.image_create_view, name='images-create'),
    path('<str:slug>', views.ImageDetailView.as_view(), name='images-detail'),
    path('upload/<str:slug>', views.imgur_upload, name='images-upload'),
    path('delete/<str:slug>', views.ImageDeleteView.as_view(), name='images-delete'),
]