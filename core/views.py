from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .forms import Upload_Form
from .models import Upload_File

FILE_TYPE = ['pdf']

def index(request):
    # form = Upload_Form()
    if request.method == 'POST':
        # f=request.FILES["pdf_file"]
        # fs = FileSystemStorage()
        # filename = fs.save(f.name, f)
        # uploaded_file_url = fs.url(filename)
        file_ = request.FILES['pdf_file']
        print("POST POST POST ")
        if request.POST.get('upload_file'):

            if not file_.name.endswith('.pdf'):
                messages.error(request, 'Please upload a .pdf file.')
            
            file_data = Upload_File(pdf_file=file_)
            file_data.save()

            # form = Upload_Form(request.POST, request.FILES)
            # if form.is_valid():
            #     user_pr = form.save(commit=False)
            #     user_pr.pdf_file = request.FILES['pdf_file']
            #     file_type = user_pr.pdf_file.name.split('.')[1]
            #     file_type = file_type.lower()
            #     if file_type not in FILE_TYPE:
            #         messages.error(request, "File must in pdf format! Please Try again")
            # user_pr.save()
            # print("data saved")
            return render(request, 'index.html') 
    else:
        return render(request, 'index.html')
