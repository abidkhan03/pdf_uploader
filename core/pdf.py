import math
from datetime import datetime
from PyPDF2 import PdfReader
import fitz
import tabula
FILE_TYPE = ['pdf']

def saveImage(pdf_path:str):
        if ".pdf" in pdf_path:
            doc = fitz.Document(pdf_path)
            # for i in range(len(doc)):
            for i,img in enumerate(doc.get_page_images(0)):
                    xref = img[0]
                    image = doc.extract_image(xref)
                    pix = fitz.Pixmap(doc, xref)
                    pix.save("core/static/images/{}.png".format(i))

def getSecondPage(file_path: str):
    data={
        'userImg':"images/0.png",     #user image
        'userSign':"images/1.png",    #user signature
    }
    pdf = PdfReader(file_path)
    for page in pdf.pages:
        text=page.extractText()
        for line in text.split('\n'):
            if "National" in line.split(' '):data["NationalID"]=line.split(' ')[-1]
            elif ['Voter','At'] == line.split()[:2]: data["VoterAt"]=line.split(' ')[-1]
            elif ['Blood','Group'] == line.split()[:2]:
                if "Group"==line.split(' ')[-1]:
                    data["BloodGroup"]=""
                else:
                    data["BloodGroup"]=line.split(' ')[-1]
    return data
def CleanString(string:str):
    return string.replace('\n',' ').replace('\t',' ').replace('\r',' ')

def getFirstPage(file_path:str):
    data=getSecondPage(file_path) 
    tables = tabula.read_pdf(file_path, pages="1", multiple_tables=True, encoding='UTF')   
    for df in tables:
        if len(df.columns)>4:
            df.dropna(how='all', inplace=True,axis=1)
            df.fillna(value='',inplace=True)
            print(df.head())
            for index,row in df.iterrows():
                if row[0]=='Pin':
                    data[row[0]]=row[1]
                elif row[0]=='Name(Bangla)':
                    data['NameB']=row[1]
                elif row[0]=='Name(English)':
                    data['NameE']=row[1]
                elif row[0]=='Father Name':
                    data['FatherName']=row[1]
                elif row[0]=='Mother Name':
                    data['MotherName']=row[1]
                elif row[0]=='Date of Birth':
                    data['DOB']=datetime.strptime(row[1],'%Y-%m-%d').strftime('%d %B %Y')
                elif row[0]=='Brith Place':
                    data['BirthPlace']=row[1]
                elif row[0]=="Present Address":
                        data['Present']=dict(
                            division=row[2],
                            district=row[4],
                            CCOM=CleanString(df.iloc[index+1,4]),
                            MM=  CleanString(df.iloc[index+3,2]),
                            AMM= CleanString(df.iloc[index+3,4]),
                            VR=  CleanString(df.iloc[index+4,4]),
                            AVR= CleanString(df.iloc[index+5,2]),
                            HH=  CleanString(df.iloc[index+5,4]),
                            PostOffice=df.iloc[index+6,2],
                            PostCode=df.iloc[index+6,4],
                        )
                elif row[0]=='Permanent Address':
                        data['Permanent']=dict(
                            division=row[2],
                            district=row[4],
                            CCOM=CleanString(df.iloc[index+1,4]),
                            MM=  CleanString(df.iloc[index+3,2]),
                            AMM= CleanString(df.iloc[index+3,4]),
                            VR=  CleanString(df.iloc[index+4,4]),
                            AVR= CleanString(df.iloc[index+5,2]),
                            HH=  CleanString(df.iloc[index+5,4]),
                            PostOffice=df.iloc[index+6,2],
                            PostCode=df.iloc[index+6,4],
                        )
    data['barcode']="<pin>{}</pin><name>{}</name><DOB>{}</DOB><FP></FP><F>Right Index</F><TYPE>A</TYPE><V>2.0</V><ds>302d02147e072a6e7a9ab9d4333cf0a907b8c479e25ff67502150086df44f9a4a1ea7992fb4dc727fbb9399ea337b8</ds>".format(data['Pin'],data['NameB'],data['DOB'])
    return data

def main(file:str):
    saveImage(file)
    data=getFirstPage(file)
    return data
if __name__=="__main__":
    print(main("media/test_Bs1vYdW.pdf"))


# from django.shortcuts import render
# from django.http import  HttpResponseRedirect
# from django.urls import reverse
# from django.core.files.storage import FileSystemStorage
# from django.contrib import messages
# from .pdf import main,FILE_TYPE,saveImage
# import os
# def index(request):
#     # form = Upload_Form()
#     # print(request.FILES)
#     # print(request.FILES)
#     # print(request.FILES)
#     # print(request.FILES)
#     if request.method == 'POST':
#         # print(request.FILES)
#         if request.FILES:
#             f=request.FILES["pdf_file"]
#             # print(f.name)
#             fs = FileSystemStorage()
#             fs.url = fs.base_url + f.name
#             if fs.url.split('.')[-1] not in FILE_TYPE:
#                 messages.error(request, 'File type not allowed')
#                 return HttpResponseRedirect(reverse('index'))
#             else:
#                 fs.save("test.pdf", f)
#                 saveImage('media/test.pdf')
#                 jsonobj=main('media/test.pdf')
#                 for file in os.listdir('media/'):
#                         os.remove('media/'+os.path.join(file))
#                 # os.remove('media/test.pdf')
#                 messages.success(request, 'File uploaded successfully')
#                 return render(request, 'index.html', {'data': jsonobj})
#         else:
#             messages.error(request, 'Please select a file')
#             return HttpResponseRedirect(reverse('index'))
#     else:
#         return render(request, 'index.html')