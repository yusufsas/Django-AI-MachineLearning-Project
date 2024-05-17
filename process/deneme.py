from transformers import AutoTokenizer, AutoModel
import torch

# Scibert modelini yükle
scibert_model_name = "allenai/scibert_scivocab_uncased"
tokenizer = AutoTokenizer.from_pretrained(scibert_model_name)
scibert_model = AutoModel.from_pretrained(scibert_model_name)

# Metni tokenize et
text = "Bir metni buraya girinkcbwsjkncwesnkc."
tokens = tokenizer.tokenize(text)

# Tokenleri tensorlara dönüştür
input_ids = tokenizer.encode(text, return_tensors="pt")
print(input_ids)
# Modelden geçir
with torch.no_grad():
    outputs = scibert_model(input_ids)
    print(outputs)

# Tuple'dan çıktıları al
hidden_states = outputs[0]

# Tokenlerin son katman çıktılarını al
last_hidden_states = hidden_states[:, 0, :]

# Vektörü numpy dizisine çevir
text_vector = last_hidden_states.numpy()
text_vector=text_vector.tolist()
# print(text_vector[0])
