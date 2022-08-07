from django import forms
from .models import Upload_File

class Upload_Form(forms.ModelForm):
    class Meta:
        model = Upload_File
        fields = ['pdf_file']