from django.contrib import admin

from software.models import Software
from .models import *
# Register your models here.


admin.site.register(Image)
admin.site.register(File)
