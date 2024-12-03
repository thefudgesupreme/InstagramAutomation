from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Image

# Create your views here.
class ImagesView(ListView):
    model = Image
    template_name = 'images/home.html'
    context_object_name = 'images'