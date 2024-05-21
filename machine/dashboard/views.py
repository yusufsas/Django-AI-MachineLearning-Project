from django.shortcuts import render,redirect
from django.http import JsonResponse
# Create your views here.
import json
from sklearn.preprocessing import MinMaxScaler
from .forms import SignUpForm,ReaderSignUpForm
from sklearn.metrics import precision_score, recall_score
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import login, authenticate
from django.shortcuts import render
from .models import FastTextVector,Reader,Interest
import numpy as np
import fasttext.util
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import torch
from django.contrib.auth.decorators import login_required

# NLTK'yi başlat
nltk.download('punkt')
nltk.download('stopwords')

# Stopwords listesini yükle
stop_words = set(stopwords.words('english'))

# Porter Stemmer'ı başlat
stemmer = PorterStemmer()
dizin_yolu = "C:/Users/yusuf/Desktop/github/yazlab2-3/Krapivin2009/keys" 
def dosya_oku_ve_kaydet(dizin_yolu):
    # Dizin içindeki .key uzantılı dosyaları bul
    for dosya_adı in os.listdir(dizin_yolu):
        if dosya_adı.endswith(".key"):
            dosya_yolu = os.path.join(dizin_yolu, dosya_adı)
            # Dosyayı aç ve satırları oku
            with open(dosya_yolu, 'r') as dosya:
                tamamlar = dosya.readlines()  # Tüm satırları al
                for tamlama in tamamlar:
                    # Satırın başındaki ve sonundaki boşlukları kaldır
                    tamlama = tamlama.strip()
                    # Her tamlamayı veritabanına ekle, eğer daha önce eklenmemişse
                    if not Interest.objects.filter(name=tamlama).exists():
                        Interest.objects.create(name=tamlama)

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



def create_vectors_from_dataset(dataset_folder, ft_model,scibert_model,tokenizer, batch_size=100):
    files = os.listdir(dataset_folder)
    total_files = len(files)
    
    for i in range(0, total_files, batch_size):
        batch_files = files[i:i+batch_size]
        vectors_to_create = []
        
        for file_name in batch_files:
            file_path = os.path.join(dataset_folder, file_name)
            
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            start_index = text.find('--T')  # Başlık başlangıç indeksi
            

            end_index = text.find('--A', start_index)  # Başlığın bitiş indeksi
    

            text2 = text[start_index+len('--T'):end_index].strip() 

            processed_text = preprocess_text(text)
            vector = ft_model.get_sentence_vector(processed_text)
            vector=vector.tolist()
            
            scibert_model_name = "allenai/scibert_scivocab_uncased"
            # tokenizer = AutoTokenizer.from_pretrained(scibert_model_name)
            # scibert_model = AutoModel.from_pretrained(scibert_model_name)
            processed_sc_text=preprocess_text(text2)
            tokens = tokenizer.tokenize(processed_sc_text)

# Tokenleri tensorlara dönüştür
            input_ids = tokenizer.encode(processed_sc_text, return_tensors="pt")

            
            with torch.no_grad():

                outputs = scibert_model(input_ids)
               
               
# Tuple'dan çıktıları al
            hidden_states = outputs[0]

# Tokenlerin son katman çıktılarını al
            last_hidden_states = hidden_states[:, 0, :]

            text_vector = last_hidden_states[:, :300]

# Vektörü numpy dizisine çevir
            text_vector = text_vector.numpy()
            text_vector=text_vector.tolist()
            text_vector=text_vector[0]
            
            id_number = file_name.split('.')[0]
            
            title=text2
            vectors_to_create.append(FastTextVector(id_number=id_number,title=title, text=processed_text,vector=vector,sc_vector=text_vector))
            
        FastTextVector.objects.bulk_create(vectors_to_create)

# Krapivin datasetinin bulunduğu klasör yolu
dataset_folder = "C:/Users/yusuf/Desktop/github/yazlab2-3/Krapivin2009/docsutf8"

# FastText modelini yükle
ft_model = fasttext.load_model("C:/Users/yusuf/Desktop/github/yazlab2-3/cc.en.300.bin")


tokenizer = AutoTokenizer.from_pretrained("C:/Users/yusuf/Desktop/github/yazlab2-3")
scibert_model = AutoModel.from_pretrained("C:/Users/yusuf/Desktop/github/yazlab2-3")
# Vektörleri oluştur ve veritabanına kaydet (part part)


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
        # user_article_vectors = [
         
        # ]
        # user_vector = np.mean(user_article_vectors, axis=0)

        
        # Ön işleme adımlarını uygula
        dosya_oku_ve_kaydet(dizin_yolu)

        create_vectors_from_dataset(dataset_folder, ft_model,scibert_model,tokenizer, batch_size=100)

        # text = preprocess_text(text)

        # ft_model = fasttext.load_model("C:/Users/yusuf/Desktop/github/yazlab2-3/cc.en.300.bin")
        # vector = ft_model.get_sentence_vector(text)
        
        # FastTextVector.objects.create(text=text, vector=vector)
        # vectors = FastTextVector.objects.all()
        # return render(request, 'myapp/show_vectors.html', {'text': text, 'vector': vector,'vectors': vectors})
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
def parse_vector(vector_str):
    # Karakter dizisini uygun formata dönüştür
    vector = [float(x) for x in vector_str.split(' ')]
    return np.array(vector)

# Örnek bir kullanıcı vektörü hesaplama fonksiyonu
def calculate_user_vector(article_vectors):
    # Karakter dizilerini uygun formata dönüştür ve bir listeye ekle
    parsed_vectors = [parse_vector(vector_str) for vector_str in article_vectors]
    
    # Tüm vektörlerin ortalamasını al
    user_vector = np.mean(parsed_vectors, axis=0)
    return user_vector

def preprocess_vector(vector_str):
    # Köşeli parantezleri ve içeriğini kaldır
    vector_str = vector_str.strip('[\]n')
    # Karakter dizisini uygun formata dönüştür
    vector = [float(x) for x in vector_str.split(',')]
    return np.array(vector)


# Örnek kullanım

 # Dosyaların bulunduğu dizinin yolu

def index(request):
    reader = request.user.reader
    if request.method == 'POST':
        if 'search' in request.POST:
            search=request.POST.get('search')
            searches=FastTextVector.objects.filter(title__contains=search)
            return render(request,'index.html',{'searches':searches})
        elif 'interestsearch' in request.POST:
            interestsearch=request.POST.get('interestsearch')
            interests=Interest.objects.filter(name__contains=interestsearch)
            return render(request,'index.html',{'interests':interests})
        elif 'interests[]' in request.POST:
            interests=request.POST.getlist('interests[]')
            for interest in interests:  
                interest=Interest.objects.get(id=interest)  
                reader.interests.add(interest)
                reader.save()

                # processed_text = preprocess_text(interest.name)
                # vector = ft_model.get_sentence_vector(processed_text)
                # vector=vector.tolist()
                # article=FastTextVector(id_number=interest.name, text=processed_text, vector=vector)
                # article.save()

                # reader.article_list.add(article)
                # reader.save()
            

    # user_article_vectors=[]
    # for article in reader.article_list.all():
    #     vector_string = article.vector.replace('[', '').replace(']', '')
    #     vector_list = vector_string.split()  # Stringi boşluklara göre böler ve bir liste oluşturur
    #     vector_float = [float(x) for x in vector_list] 
    #     user_article_vectors.extend(vector_float)

    
    # print(user_article_vectors)
    # user_vector = np.mean(user_article_vectors, axis=0)

    # all_article_vectors=FastTextVector.objects.all()

    # similarities = {}
    # for article in all_article_vectors:
    #     similarity_score = cosine_similarity([user_vector], [article.vector])[0][0]
    #     similarities[article.id_number] = similarity_score

    # # for article_name, article_vector in all_article_vectors.items():
    # #     similarity_score = cosine_similarity([user_vector], [article_vector])[0][0]
    # #     similarities[article_name] = similarity_score
    
    # # Benzerlik skorlarına göre sırala ve en yüksek benzerlik skorlarına sahip 5 makaleyi seç
    # sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:5]
    if reader.interests.exists():
        user_article_vectors = []
        for interest in reader.interests.all():
            processed_text = preprocess_text(interest.name)
            vector = ft_model.get_sentence_vector(processed_text)
            vector = vector.tolist()
            user_article_vectors.append(vector)
        
        user_articles = reader.article_list.all()
        user_article_ids = [article.id for article in user_articles]
        for article in user_articles:
            user_article_vectors.append(article.vector)
        
        # Calculate the average user vector
        user_vector = np.mean(user_article_vectors, axis=0)
        
        # Get all article vectors
        all_articles = FastTextVector.objects.all()
        all_article_vectors = [np.array(vector.vector) for vector in all_articles]
        all_article_sc_vectors = [np.array(vector.sc_vector) for vector in all_articles]
        
        user_vector = user_vector.reshape(1, -1)
        all_article_vectors = [vector.reshape(1, -1) for vector in all_article_vectors]
        all_article_sc_vectors = [vector.reshape(1, -1) for vector in all_article_sc_vectors]
        
        similarities = [cosine_similarity(user_vector, vector)[0][0] for vector in all_article_vectors]
        sc_similarities = [cosine_similarity(user_vector, vector)[0][0] for vector in all_article_sc_vectors]
        
        top_similarities_indices = np.argsort(similarities)[-5:][::-1]
        top_similarities_sc_indices = np.argsort(sc_similarities)[-5:][::-1]
        
        recommended_articles = FastTextVector.objects.filter(id__in=top_similarities_indices)
        recommended_sc_articles = FastTextVector.objects.filter(id__in=top_similarities_sc_indices)
        
        # Performance evaluation
        recommended_article_ids = [article.id for article in recommended_articles]
        recommended_sc_article_ids = [article.id for article in recommended_sc_articles]
        
        y_true = [1 if article.id in user_article_ids else 0 for article in all_articles]
        y_pred = [1 if article.id in recommended_article_ids else 0 for article in all_articles]
        y_pred_sc = [1 if article.id in recommended_sc_article_ids else 0 for article in all_articles]
        
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        sc_precision = precision_score(y_true, y_pred_sc)
        sc_recall = recall_score(y_true, y_pred_sc)
        
        context = {
            'reader': reader,
            'recommended_articles': recommended_articles,
            'recommended_sc_articles': recommended_sc_articles,
            'precision': precision,
            'recall': recall,
            'sc_precision': sc_precision,
            'sc_recall': sc_recall
        }
        
        return render(request, 'index.html', context)


   
    return render(request,'index.html',{'reader':reader})


# def dashboard(request):
    
#     return render(request,'dashboard.html')
@login_required
def like_article(request, id):
    fasttextvector = FastTextVector.objects.get(id=id)
    reader = Reader.objects.get(user=request.user)
    
    # Eğer fasttextvector zaten article_list içinde yoksa, ekle
    if not reader.article_list.filter(id=id).exists():
        reader.article_list.add(fasttextvector)
    
    return redirect('index')

@login_required
def dislike_article(request, id):
    fasttextvector = FastTextVector.objects.get(id=id)
    reader = Reader.objects.get(user=request.user)
    
    # Eğer fasttextvector article_list içinde varsa, çıkar
    if reader.article_list.filter(id=id).exists():
        reader.article_list.remove(fasttextvector)
    
    return redirect('index')


def detail(request,id):
    fasttextvector = FastTextVector.objects.get(id=id)
    reader = Reader.objects.get(user=request.user)

# Eğer fasttextvector zaten article_list içinde yoksa, ekle
    if not reader.article_list.filter(id=id).exists():
        reader.article_list.add(fasttextvector)
    filesdırs='C:/Users/yusuf/Desktop/github/yazlab2-3/Krapivin2009/docsutf8/'
    target=fasttextvector.id_number+'.txt'
    file_path = os.path.join(filesdırs, target)


    
    if os.path.exists(file_path):
    # Dosyayı açın ve içeriğini okuyun
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

    # Title, abstract ve body bölümlerini ayırmak için işaretleyicileri kullanın
        title_start = text.find('--T')
        abstract_start = text.find('--A')
        body_start = text.find('--B')

        if title_start != -1 and abstract_start != -1 and body_start != -1:
            title = text[title_start + 3:abstract_start].strip()
            abstract = text[abstract_start + 3:body_start].strip()
            body = text[body_start + 3:].strip()
            return render(request,'detail.html',{'fasttextvector':fasttextvector,"title":title,'abstract':abstract,'body':body})
        # print("Title:\n", title)
        # print("\nAbstract:\n", abstract)
        # print("\nBody:\n", body)
        else:
            print("Metin içindeki işaretleyiciler eksik veya hatalı.")
    
    else:
        print(f"'{target}' adlı dosya bulunamadı.")


    return render(request,'detail.html',{'fasttextvector':fasttextvector})





