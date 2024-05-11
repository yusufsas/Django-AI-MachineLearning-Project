from django.shortcuts import render,redirect
from django.http import JsonResponse
# Create your views here.
from .forms import SignUpForm,ReaderSignUpForm
# from rest_framework.response import Response 
from django.contrib.auth.forms import AuthenticationForm
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .serializers import UserSerializer
from django.contrib.auth import login, authenticate
from django.shortcuts import render
from .models import FastTextVector

import fasttext.util

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string

# NLTK'yi başlat
nltk.download('punkt')
nltk.download('stopwords')

# Stopwords listesini yükle
stop_words = set(stopwords.words('english'))

# Porter Stemmer'ı başlat
stemmer = PorterStemmer()

def preprocess_text(text):
    # Küçük harfe dönüştür
    text = text.lower()
    
    # Noktalama işaretlerini kaldır
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Metni kelimelere ayır
    words = word_tokenize(text)
    
    # Stopwords'leri ve tek harfli kelimeleri kaldır
    words = [word for word in words if word not in stop_words and len(word) > 1]
    
    # Kelimeleri birleştir
    text = ' '.join(words)
    
    # Kelime köklerini bul
    text = stemmer.stem(text)
    
    return text

# Örnek metin
# text = "Before converting the word to vectors in fasttext, a Python code that removes stopwords with NLTK, removes punctuation marks, and finds the roots of words."

# Ön işleme adımlarını uygula
# processed_text = preprocess_text(text)
# print(processed_text)

  
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

def create_vector(request):
    if request.method == 'POST':
        text = request.POST['text']
        # fasttext.util.download_model('en', if_exists='ignore') 
        # ft_model = fasttext.load_model('cc.en.300.bin')
        # text = "Before converting the word to vectors in fasttext, a Python code that removes stopwords with NLTK, removes punctuation marks, and finds the roots of words."

        # Ön işleme adımlarını uygula
        text = preprocess_text(text)

        ft_model = fasttext.load_model("C:/Users/yusuf/Desktop/github/yazlab2-3/cc.en.300.bin")
        vector = ft_model.get_sentence_vector(text)
        
        FastTextVector.objects.create(text=text, vector=vector)
        vectors = FastTextVector.objects.all()
        return render(request, 'myapp/show_vectors.html', {'text': text, 'vector': vector,'vectors': vectors})
    return render(request, 'myapp/create_vector.html')



def show_vectors(request):
    vectors = FastTextVector.objects.all()
    return render(request, 'myapp/show_vectors.html', {'vectors': vectors})

# def create_vector(request):
#     if request.method == 'POST':
#         text = request.POST['text']
#         # FastText modelinizi yükleyin ve metin için vektörü alın
#         model = fasttext.load_model('./fastText/python/fasttext_module')
#         vector = model.get_sentence_vector(text)
#         # Veritabanına kaydet
#         FastTextVector.objects.create(text=text, vector=vector)
#         return render(request, 'myapp/result.html', {'text': text, 'vector': vector})
#     return render(request, 'myapp/create_vector.html')

def index(request):
    if request.method == 'POST':
        search=request.POST.get('search')
        return render(request,'index.html',{'search':search})


    return render(request,'index.html')


def dashboard(request):
    
    return render(request,'dashboard.html')



# def signup(request):


#     return render(request,'signup.html')



def user_login(request):


    return render(request,'user_login.html')




def hello(request):

    
    return JsonResponse({'message': 'Hello AŞKIM!'})



