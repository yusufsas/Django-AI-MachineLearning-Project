from django.shortcuts import render,redirect
from django.http import JsonResponse
# Create your views here.
from .forms import SignUpForm,ReaderSignUpForm
from rest_framework.response import Response 
from django.contrib.auth.forms import AuthenticationForm
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth import login, authenticate
# @api_view(['POST'])
# def signup(request):
#     if request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def signup(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        client_form = ReaderSignUpForm(request.POST)
        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save()
            client = client_form.save(commit=False)
            client.user = user
            client.save()
            login(request, user)
            return redirect('reader_login')  # veya başka bir sayfaya yönlendirme yapabilirsiniz
    else:
        user_form = SignUpForm()
        client_form = ReaderSignUpForm()
    return render(request, 'registration/signup.html', {'user_form': user_form, 'client_form': client_form})

def reader_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/user_login.html', {'form': form})




def index(request):


    return render(request,'index.html')


def dashboard(request):
    
    return render(request,'dashboard.html')



# def signup(request):


#     return render(request,'signup.html')



def user_login(request):


    return render(request,'user_login.html')




def hello(request):

    
    return JsonResponse({'message': 'Hello AŞKIM!'})



