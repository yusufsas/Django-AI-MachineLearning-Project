from django.contrib import admin
from django.urls import path
from .views import index,signup,detail

urlpatterns =[

    path('',index,name='index'),
    path('detail/<int:id>',detail,name='detail'),

    # path('signup/', signup),
]