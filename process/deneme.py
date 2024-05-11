from gensim.models import FastText
import numpy as np

# 100 tane örnek cümle
sentences = [
    "Bu bir örnek cümledir.",
    "Örnek bir cümle oluşturduk.",
    "Bu bir örnek cümledir.",
    "Örnek bir cümle oluşturduk.",
    "FastText vektör temsilleri için örnek kod yazıyoruz.",
    "Metin işleme yöntemleri hakkında örnekler inceliyoruz.",
    "Python programlama dili kullanarak örnekler geliştiriyoruz.",
    # Diğer cümleler buraya eklenebilir...
]

# FastText modelini eğitme
model = FastText([sentence.split() for sentence in sentences], min_count=1, workers=4)

# Her cümle için vektör temsillerini oluşturma
sentence_vectors = []
for sentence in sentences:
    word_vectors = [model.wv.get_vector(word) for word in sentence.split() if word in model.wv.key_to_index]
    if word_vectors:
        sentence_vector = np.mean(word_vectors, axis=0)
        sentence_vectors.append(sentence_vector)
    else:
        # Eğer cümlede modelde olmayan bir kelime varsa, vektörü None olarak ayarlayabilirsiniz.
        # sentence_vectors.append(None)
        # veya bu cümleyi tamamen atlayabilirsiniz.
        pass

# Her cümle için oluşturulan vektörleri yazdırma
for i, vector in enumerate(sentence_vectors):
    print(f"Cümle {i+1} vektör temsili:")
    print(vector)
