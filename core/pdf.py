from PyPDF2 import PdfReader
import fitz
import io
from PIL import Image

FILE_TYPE = ['pdf']
def getImage(pdf_path:str):
    # pdf_file = fitz.open(pdf_path)
    # page = pdf_file[0]
    # print(pdf_file)
    # img_list=page.getImageList()
    # for img in img_list:
    #     pix=img[1]
    #     pix.writePNG("images/{}.png".format(img[0]))
        if ".pdf" in pdf_path:
            doc = fitz.Document(pdf_path)
            # for i in range(len(doc)):
            for i,img in enumerate(doc.get_page_images(0)):
                    xref = img[0]
                    image = doc.extract_image(xref)
                    pix = fitz.Pixmap(doc, xref)
                    pix.save("core/static/images/{}.png".format(i))
                    
        print("Done!")



def JsonParser(pdf: PdfReader):
    obj={
        'userImg':"images/0.png",     #user image
        'userSign':"images/1.png",    #user signature

    }
    for page in pdf.pages:
        text=page.extractText()
        for index,line in enumerate(text.split('\n')):
            print(line)
            if "National" in line.split(' '):obj["NationalID"]=line.split(' ')[-1]
            elif "Pin" in line.split(' '):obj["Pin"]=line.split(' ')[-1]
            elif "Name(Bangla)" in line.split(' '): obj["NameBangla"]=" ".join(line.split(' ')[2:])
            elif "Name(English)" in line.split(' '): obj["NameEnglish"]=" ".join(line.split(' ')[1:])
            elif ['Date', 'of', 'Birth'] == line.split()[:3]: obj["DOB"]=line.split(' ')[-1]
            elif ['Father','Name'] == line.split()[:2]: obj["FatherName"]=" ".join(line.split(' ')[2:])
            elif ['Mother','Name'] == line.split()[:2]: obj["MotherName"]=" ".join(line.split(' ')[2:])
            elif ['Birth','Place'] == line.split()[:2]: obj["BirthPlace"]=" ".join(line.split(' ')[2:])
            elif "Village/R" in line.split():
                village=line.split("oad")[-1].split("Home")[0]
                home=text.split('\n')[index+1][2:].split(' ')
                home.append(text.split('\n')[index+2].split(' ')[0])
                obj["Village"]=village
                obj["Home"]=" ".join(home)
            elif ['Post','Office'] == line.split()[:2]:
                post=line.split('Office')[-1].split('Postal')[0]
                obj["PostOffice"]=post
            elif ['Blood','Group'] == line.split()[:2]:
                obj["BloodGroup"]=line.split(' ')[-1]
                
            
    return obj
def GetPdf(file_path:str):
    pdf = PdfReader(file_path)
    jsonobj=JsonParser(pdf)
    # print(jsonobj)
    return jsonobj


if __name__ == '__main__':
    getImage('media/test.pdf')
    GetPdf('media/test.pdf')
    