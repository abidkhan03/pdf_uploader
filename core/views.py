from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import Upload_File
from PyPDF2 import PdfReader

FILE_TYPE = ['pdf']

def index(request):
    # form = Upload_Form()
    if request.method == 'POST':
        f=request.FILES["pdf_file"]
        fs = FileSystemStorage()
        filename = fs.save(f.name, f)
        uploaded_file_url = fs.url(filename)

        if request.POST.get('upload_button'):
            print("POST Upload File ")
            if filename not in FILE_TYPE:
                messages.error(request, 'Please upload a .pdf file.')
            
            file_data = Upload_File(pdf_file=filename)
            file_data.save()
            return HttpResponse('<h1>File Uploaded Successfully!</h1>')

        if request.POST.get('generate_button', False):
            pdf = Upload_File.objects.all().first()
            reader = PdfReader(settings.MEDIA_ROOT + '/' + pdf.pdf_file.name)
            text = ""
            for page in reader.pages:
                text += page.extractText()
            print(text)
    else:
        # pdf = Upload_File.objects.all().last()
        # reader = PdfReader(settings.MEDIA_ROOT + '/' + pdf.pdf_file.name)
        # text = ""
        # for page in reader.pages:
        #     text += page.extractText()
        # print(text)
        return render(request, 'index.html')
