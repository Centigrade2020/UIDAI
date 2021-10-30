from django.db import models
import qrcode
import qrcode.image.svg
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

# Create your models here


class qr(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    image = models.ImageField(upload_to='images',blank=True)
    qr_code = models.ImageField(upload_to = 'qr_codes',blank = True)

    def __str__(self):
        return str(self.name) or self.id

    def save(self):
        if self.name:
            qrcode_img = qrcode.make(self.name)
        else:
            qrcode_img =qrcode.make(self.image)
        canvas = Image.new('RGB',(1000,1000),'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.name}' + '.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save = False)
        canvas.close()
        super().save()

