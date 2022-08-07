from django.db import models


class Upload_File(models.Model):
    pdf_file = models.FileField(upload_to='media/') 

