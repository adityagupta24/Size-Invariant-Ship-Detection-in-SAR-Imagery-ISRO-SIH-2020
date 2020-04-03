from django.http import HttpResponse 
from django.shortcuts import render, redirect
import os
from .forms import *
from django.views.generic import TemplateView
import os
# Create your views here.

class Index(TemplateView):
    template_name = 'home/index.html'

def ShipDetection_view(request):
    if request.method == 'POST': 
        form = ShipForm(request.POST, request.FILES) 
  
        if form.is_valid(): 
            form.save() 
            # return redirect('result')
            scale = request.POST.get("scale")
            for i in range(10):
                print(scale)
            # request.session['scale'] = scale
            return predict(request, scale)
            # return redirect('predict', scale)
            # return render(request, 'home/display_images.html') 
            # return redirect('process', {'scale' : scale})
    else:
        print(os.getcwd())
        os.system('rm -r ./media/images/')
        form = ShipForm() 
    return render(request, 'home/im.html', {'form' : form}) 

  
def predict(request, scale): 
    for i in range(10):
        print(scale)
    # os.system('deactivate')
    # return 
    # print(BASE_DIR)
    # print(os.getcwd())
    path = os.getcwd()

    ls = os.listdir('./media/images/')
    # print(path)
    # scale = request.session['scale']
    # scale = 2
    os.chdir(path + '/home/model/SIH5/model/darknet/')
    os.system('python3 r3unfile.py ' + path + '/media/images/' + str(ls[0] + ' ' + path) + ' ' + str(scale))
    # print('path:', path)
    os.chdir(path + '/')
    # os.system('python3 r2unfile.py')
    # os.system('source env/bin/activate')
    return render(request, 'home/display_images.html')


def Upload(request):
    image = request.POST.get('image')
    print(type(image))
    # os.chdir('/Users/gauravverma/Library/Containers/com.apple.STMExtension.Mail/Data/Documents/SIH5/model/darknet/')
    # os.system('python3 r2unfile.py')
    return render(request, 'home/upload_image.html')

def display_ship_images(request): 
  
    if request.method == 'GET': 
        return render(request, 'home/display_images.html')
