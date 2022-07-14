from django.db import models
from stdimage import StdImageField, JPEGField
from django.db.models.fields.files import FileField

# Create your models here.


class Image (models.Model):
    name = models.CharField(max_length=254, blank=True, null=True)
    file = StdImageField(
        upload_to='images/%y/%m/%d',
        blank=True,
        variations={
            'thumbnail': (100, 100, True),
            'large': (600, 400),
            'medium': (300, 200),
        },
        delete_orphans=True
    )

    def int(self):
        return self.id


class File (models.Model):
    name = models.CharField(max_length=254, blank=True, null=True)
    file = FileField(upload_to='documents/%y/%m/%d')

    def __str__(self):
        return self.name
