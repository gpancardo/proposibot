import unicodedata
import re
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')

class Preprocessor:
    def __init__(self):
        self.no_special_chars = re.compile(r'[^\w\s]')

        #Quantifiers
        self.quantifiers = {
            'todos': 'CUANT_TODO', 'todas': 'CUANT_TODO', 'todo': 'CUANT_TODO', 'toda': 'CUANT_TODO',
            'ningun': 'CUANT_NINGUN', 'ninguna': 'CUANT_NINGUN', 'ningunos': 'CUANT_NINGUN', 'ningunas': 'CUANT_NINGUN',
            'algunos': 'CUANT_ALGUNOS', 'algunas': 'CUANT_ALGUNOS', 'algun': 'CUANT_ALGUNOS', 'alguna': 'CUANT_ALGUNOS',
            'ciertos': 'CUANT_ALGUNOS', 'ciertas': 'CUANT_ALGUNOS', 'cierto': 'CUANT_ALGUNOS', 'cierta': 'CUANT_ALGUNOS'
        }

        self.relation_verbs = {'es', 'son', 'fue', 'fueron', 'sera', 'seran', 'seria', 'serian'}
        self.negation_terms = {'no', 'ni', 'nunca', 'jamas', 'sin'}

        # Stopwords - negation
        self.stopwords_es = {self.normalize_text(w) for w in stopwords.words('spanish')}
        self.stopwords_es -= self.negation_terms
    
    # Normalization
    def normalize_text(self, text):
        text = text.lower()
        text = ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )
        return self.no_special_chars.sub("", text)

    #Term extraction
    def extract_terms(self, text):
        tokens = self.normalize_text(text).split()
        terms = []

        for token in tokens:
            if token in self.stopwords_es:
                continue
            terms.append(token)

        return terms

    def preprocess(self, text):
        tokens = self.normalize_text(text).split()
        processed_tokens = []

        for token in tokens:
            if token in self.negation_terms:
                processed_tokens.append("NEGACION")
            elif token in self.quantifiers:
                processed_tokens.append(self.quantifiers[token])
            elif token in self.relation_verbs:
                processed_tokens.append("VERBO_RELACION")
            elif token in self.stopwords_es:
                continue
            else:
                processed_tokens.append("TERMINO")

        return " ".join(processed_tokens)
