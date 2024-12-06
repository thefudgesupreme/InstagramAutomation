from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['image'] = self.object
    #     return context

def imgur_upload(request, slug):
    image = Image.objects.get(slug=slug)
    print(f'slug: {slug}')
    uploaded, link=post_image(image.title, "", image.image.path)
    if uploaded:
        image.imgur_uploaded = uploaded
        image.imgur_url = link
        image.save()
    else:
        messages.add_message(request, messages.ERROR, 'Changes successfully saved.')
    return redirect(to=f'/images/{image.slug}', permanent=False)

