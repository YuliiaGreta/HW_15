import re

import re

def clean_text(text):
    # Удаляет небуквенные символы и приводит текст к нижнему регистру
    cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text).lower()
    return cleaned_text.strip()


def remove_stop_words(text, stop_words):
    # Удаляет стоп-слова из текста
    words = text.split()
    return ' '.join([word for word in words if word not in stop_words])