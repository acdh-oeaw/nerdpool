from django.contrib import admin

from . models import *
# Register your models here.
admin.site.register(Dataset)
admin.site.register(Example)
admin.site.register(ProdigyServer)
admin.site.register(NerSample)
