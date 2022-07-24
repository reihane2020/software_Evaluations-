from django.db import models

# Create your models here.


class SoftwareArea(models.Model):
    name = models.CharField(max_length=254, blank=False, null=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SoftwareSection(models.Model):
    title = models.CharField(max_length=254)

    def __str__(self):
        return self.title


class Software(models.Model):
    name = models.CharField(max_length=150, null=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    logo = models.ForeignKey(
        "upload.Image", on_delete=models.SET_NULL, blank=True, null=True
    )
    rating = models.DecimalField(
        max_digits=3, decimal_places=2, null=True, blank=True,
    )
    created_by = models.ForeignKey(
        "authentication.Account", on_delete=models.CASCADE, null=False, blank=False
    )
    area = models.ForeignKey(
        SoftwareArea, on_delete=models.SET_NULL, null=True, blank=True
    )
    sections = models.ManyToManyField(SoftwareSection,  blank=True)
    download_link = models.CharField(max_length=1000)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
