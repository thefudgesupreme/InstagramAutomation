from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView
from .models import Image

# Create your views here.
class ImagesView(ListView):
    model = Image
    template_name = 'images/home.html'
    context_object_name = 'images'

class ImageCreateView(CreateView):
    model = Image
    fields = ['title', 'image', ]
    template_name = 'images/create.html'
    success_url = '/images/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class ImageDetailView(DetailView):
    model = Image
    template_name = 'images/detail.html'
    context_object_name = 'image'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['image'] = self.object
    #     return context