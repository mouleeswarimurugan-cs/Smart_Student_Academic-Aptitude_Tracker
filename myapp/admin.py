from django.contrib import admin
from myapp.models import *
# Register your models here.

admin.site.register(Subject)
admin.site.register(Assignment)
admin.site.register(AptitudeCategory)
admin.site.register(Question)