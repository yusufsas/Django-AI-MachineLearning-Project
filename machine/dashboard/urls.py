from django.contrib import admin
from django.urls import path
from .views import index,signup

urlpatterns =[

    path('',index,name='index'),
    # path('signup/', signup),
]