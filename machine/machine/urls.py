"""machine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from dashboard.views import index,signup,hello,reader_login,create_vector,show_vectors
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/',include('dashboard.urls')),
    # path('',index,name='index'),
    path('',signup,name='signup'),
    path('reader_login/', reader_login, name='reader_login'),
    path('create_vector/', create_vector, name='create_vectors'),
    path('show_vector/', show_vectors, name='show_vector'),
    # path('signup/',signup,name='signup'),
    path('api', hello, name='hello'),
    # path('api/', include('users.urls')),

    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
