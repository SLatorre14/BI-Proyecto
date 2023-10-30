from sklearn.base import BaseEstimator, TransformerMixin
from nltk import word_tokenize
from nltk.corpus import stopwords
import re, string, unicodedata
import pandas as pd
from num2words import num2words
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from sklearn.pipeline import Pipeline

def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = LancasterStemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems

def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas

def stem_and_lemmatize(words):
    stems = stem_words(words)
    lemmas = lemmatize_verbs(words)
    return stems + lemmas

def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words

def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

def replace_numbers(words):
    """Replace all interger occurrences in list of tokenized words with textual representation"""    
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = num2words(word, lang='es')            
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words

def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    
    new_words = []
    stop_words = set(stopwords.words('spanish'))
    
    for word in words:
        if word not in stop_words:
            new_words.append(word)
    return new_words

def preprocessing(words):
    words = to_lowercase(words)
    words = replace_numbers(words)
    words = remove_punctuation(words)
    words = remove_non_ascii(words)
    words = remove_stopwords(words)
    return words


class lecturaDatos(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
        
    def transform(self, archivocsv, y=None):
        data=pd.read_excel(archivocsv, engine='xlrd')
        return data

class limpiezayTokenDatos(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
        
    def transform(self, data, y=None):
        data['palabras'] = data['Textos_espanol'].apply(word_tokenize).apply(preprocessing)
        return data
    
class normalizacion(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
        
    def transform(self, data, y=None):
        data['palabras'] = data['palabras'].apply(stem_and_lemmatize) #Aplica lematización y Eliminación de Prefijos y Sufijos.
        return data
    
class seleccion(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
        
    def transform(self, data, y=None):
        data['palabras'] = data['palabras'].apply(lambda x: ' '.join(map(str, x)))
        return data
    

pipeLimpieza = Pipeline(
    steps=[
        ("Limpieza", limpiezayTokenDatos()),
        ("Normalizacion", normalizacion()),
        ("Seleccion", seleccion()),
    ]
)