from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Reader,Interest,FastTextVector
# Register your models here.


admin.site.register(Interest)
admin.site.register(Reader)
admin.site.register(FastTextVector)