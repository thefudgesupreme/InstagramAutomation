from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic import DeleteView
from django.views.generic.edit import CreateView
from .models import Image
from .imgur_upload import post_image
from django.contrib import messages

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

class ImageDeleteView(DeleteView):
    model = Image
    template_name = 'images/delete.html'
    success_url = '/images/'

    def get_object(self):
        return get_object_or_404(Image, slug=self.kwargs['slug'])

def imgur_upload(request, slug):
    image = Image.objects.get(slug=slug)
    print(f'slug: {slug}')
    uploaded, link=post_image(image.title, "", image.image.path)
    if uploaded:
        image.imgur_uploaded = uploaded
        image.imgur_url = link
        image.save()
        print("Upload successful")
        messages.add_message(request, messages.SUCCESS, 'Upload successful')
    else:
        print("Upload failed")
        messages.add_message(request, messages.ERROR, 'Upload failed')
    return redirect(to=f'/images/{image.slug}', permanent=False)

