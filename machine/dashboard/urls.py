from django.contrib import admin
from django.urls import path
from .views import index,signup,detail,like_article,dislike_article

urlpatterns =[

    path('',index,name='index'),
    path('detail/<int:id>',detail,name='detail'),
    path('like/<int:id>/', like_article, name='like_article'),
    path('dislike/<int:id>/', dislike_article, name='dislike_article'),

    # path('signup/', signup),
]