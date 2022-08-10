from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import Upload_File
from PyPDF2 import PdfReader
import fitz
import io
from PIL import Image

FILE_TYPE = ['pdf']
def getImage(pdf_path:str):
    pdf_file = fitz.open(pdf_path)
    page = pdf_file[0]
    img_list=page.getImageList()
    for img in img_list:
        pix=img[1]
        pix.writePNG("images/{}.png".format(img[0]))
    
def JsonParser(pdf: PdfReader):
    return pdf.pages[0].extractText()
def GetPdf(file_path:str):
    pdf = PdfReader(file_path)
    jsonobj=JsonParser(pdf)
    print(jsonobj)
    return jsonobj



def index(request):
    # form = Upload_Form()
    if request.method == 'POST':
        f=request.FILES["pdf_file"]
        fs = FileSystemStorage()
        fs.url = fs.base_url + f.name
        if fs.url.split('.')[-1] not in FILE_TYPE:
            messages.error(request, 'File type not allowed')
            return HttpResponseRedirect(reverse('index'))
        else:
            fs.save(f.name, f)
            print(fs.url)
            messages.success(request, 'File uploaded successfully')
            return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'index.html')
