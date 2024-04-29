from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.



def index(request):


    return render(request,'index.html')


def dashboard(request):
    
    return render(request,'dsahboard.html')



def signup(request):


    return render(request,'signup.html')



def user_login(request):


    return render(request,'user_login.html')




def hello(request):

    
    return JsonResponse({'message': 'Hello AŞKIM!'})



