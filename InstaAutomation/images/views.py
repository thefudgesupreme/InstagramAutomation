from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic import DeleteView
from django.views.generic.edit import CreateView
from .Gemini import Gemini
import PIL.Image

from IPython.display import Markdown
from .forms import ImageForm
from .models import Image
from .imgur_upload import post_image
from django.contrib import messages

BASE_PROMPT='''
Act as Instagram description writer.
I'll give you an image.

With the help of understand the image and write a title and description for the optimized Instagram post as well as Facebook Page.
Description should be engaging, fun to read and should hook user to read it completely.

Tips for Description:
1. Use conversational voice and tone.
2. Imagine you're talking to a friend and use natural language and phrasing.
3. Use vivid language to create imagery and atmosphere. Use metaphors, and personification.
4. Use emojis to keep description funny & engaging. 
5. Create a short 2-3 sentences story or scenario to hook users. Do not create long stories. Do not use more than 2-3 sentences.
6. Generate diffeent types of descriptions like narrative, poetic, humorous etc to keep it interesting.
7. Do not repeat same type of description for multiple images.
8. Note that output language of description will be english.You can include some words as per the context of the image from different ancient languages like Latin, Greek, 
   Germanic languages(Old/Middle English, Old Norse, Dutch), French. 
9. If you are adding words that are not in english, please add english translation in brackets next to it.
10. Check history of images already described to not repeat similar descriptions.

Tips for Title:
1. For generating Titles playful tone. Tittle should be captivating & catch attention.
2. Note that output language will be english.You can include some words as per the context of the image from different ancient languages like Latin, Greek, 
   Germanic languages(Old/Middle English, Old Norse, Dutch), French. 
3. If you are adding words that are not in english, please add english translation in brackets next to it.
4. Add relevant 1 emoji at the start and 1 emoji at the end of the title.
5. Check history of images already described to not repeat similar title.

DO NOT CREATE LONG DESCRIPTIONS. KEEP IT SHORT AND CONCISE.
Output Format - Title: [Your generated Title] Description: [Your generated Description] 
Strictly follow the output format.
Provide description for Instagram.
                  '''

# Create your views here.
class ImagesView(ListView):
    model = Image
    template_name = 'images/home.html'
    context_object_name = 'images'
def image_create_view(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        files=request.FILES.getlist('image')
        if form.is_valid():
            for f in files:
                image = Image(image=f)
                image.save()
                 
                del image
            return redirect('images-home')
    else:
        form = ImageForm()
    return render(request, 'images/create.html', {'form': form})
    
    
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
    
def image_process_view(request, slug):
    prompt=[]
    image = Image.objects.get(slug=slug)

    if not image.title or not image.description:
        gemini = Gemini(vision=True, creative=True)
        img=PIL.Image.open(image.image.path)

        prompt.append([BASE_PROMPT, img])
        responses = gemini.chat(prompt)
        response=Markdown(responses[0].text)

        print(response.data)
        if not response.data:
            messages.add_message(request, messages.ERROR, 'Error generating title or description')
            return redirect(to=f'/images/{image.slug}', permanent=True)
        title=response.data.split('Description:')[0].split(':')[1].strip()
        description=response.data.split('Description:')[1].strip()

        if not image.title:
            image.title = title
        if not image.description:
            image.description = description
         
        # Bypass validation for now
        # image.description = description
        # image.title = title
        image.save()
    return redirect(to=f'/images/{image.slug}', permanent=True)
    

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

