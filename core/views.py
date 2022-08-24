import time
from django.shortcuts import render
from django.http import  HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .pdf import getFirstPage,FILE_TYPE,saveImage
import concurrent.futures
from django.template.response import TemplateResponse
import os
# def my_render_callback(response):
#     # Do content-sensitive processing
#     jsonobj=threading.Thread(target=getFirstPage,args=('media/test.pdf',))
#     jsonobj.start()
#     return jsonobj.join()

def DeleteFile():
    for file in os.listdir('media/'):
        os.remove('media/'+os.path.join(file))

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
                # Create a response
                # response = TemplateResponse(request, 'mytemplate.html', {})
                # response.add_post_render_callback(my_render_callback)
                for file in os.listdir('media/'):
                    os.remove('media/'+os.path.join(file))
                fs.save("test.pdf", f)
                saveImage('media/test.pdf')
                # jsonobj=threading.Thread(target=getFirstPage,args=('media/test.pdf',)).start()
                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                    jsonobj=executor.submit(getFirstPage,'media/test.pdf')
                    jsonobj=jsonobj.result()
                    executor.submit(DeleteFile)
                    executor.shutdown(wait=True)
                    messages.success(request, 'File uploaded successfully')
                    # return response
                    return render(request, 'index.html', {'data': jsonobj})
        else:
            messages.error(request, 'Please select a file')
            return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'index.html')
