import re

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text.lower().strip()

def remove_stop_words(text, stop_words):
    words = text.split()
    return ' '.join([word for word in words if word not in stop_words])