from transformers import AutoTokenizer, AutoModel

# SciBERT modeli ve tokenizer'ını indir ve yükle
scibert_model_name = "allenai/scibert_scivocab_uncased"
tokenizer = AutoTokenizer.from_pretrained(scibert_model_name)
scibert_model = AutoModel.from_pretrained(scibert_model_name)

# Modeli ve tokenizer'ı daha sonra kullanmak üzere sakla
tokenizer.save_pretrained("C:/Users/yusuf/Desktop/github/yazlab2-3")
scibert_model.save_pretrained("C:/Users/yusuf/Desktop/github/yazlab2-3")