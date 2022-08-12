from django.shortcuts import render
from django.http import  HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .pdf import getImage,GetPdf,FILE_TYPE
import os
def index(request):
    # form = Upload_Form()
    if request.method == 'POST':
        if request.FILES:
            f=request.FILES["pdf_file"]
            fs = FileSystemStorage()
            fs.url = fs.base_url + f.name
            if fs.url.split('.')[-1] not in FILE_TYPE:
                messages.error(request, 'File type not allowed')
                return HttpResponseRedirect(reverse('index'))
            else:
                fs.save("test.pdf", f)
                getImage('media/test.pdf')
                jsonobj=GetPdf('media/test.pdf')
                os.remove('media/test.pdf')
                messages.success(request, 'File uploaded successfully')
                return render(request, 'index.html', {'data': jsonobj})
        else:
            messages.error(request, 'Please select a file')
            return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'index.html')
