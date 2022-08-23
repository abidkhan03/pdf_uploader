from django.shortcuts import render
from django.http import  HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .pdf import main,FILE_TYPE,saveImage
import os
def index(request):
    # form = Upload_Form()
    # print(request.FILES)
    # print(request.FILES)
    # print(request.FILES)
    # print(request.FILES)
    if request.method == 'POST':
        # print(request.FILES)
        if request.FILES:
            f=request.FILES["pdf_file"]
            # print(f.name)
            fs = FileSystemStorage()
            fs.url = fs.base_url + f.name
            if fs.url.split('.')[-1] not in FILE_TYPE:
                messages.error(request, 'File type not allowed')
                return HttpResponseRedirect(reverse('index'))
            else:
                fs.save("test.pdf", f)
                saveImage('media/test.pdf')
                jsonobj=main('media/test.pdf')
                for file in os.listdir('media/'):
                        os.remove('media/'+os.path.join(file))
                # os.remove('media/test.pdf')
                messages.success(request, 'File uploaded successfully')
                return render(request, 'index.html', {'data': jsonobj})
        else:
            messages.error(request, 'Please select a file')
            return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'index.html')
