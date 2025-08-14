import unicodedata
from nltk.corpus import stopwords
import re


class Preprocessor:
    def __init__(self):
        # Quantifiers
        self.quantifiers = {
            'todos': 'CUANT_TODO', 'todas': 'CUANT_TODO', 'todo': 'CUANT_TODO', 'toda': 'CUANT_TODO',
            'ningún': 'CUANT_NINGUN', 'ninguna': 'CUANT_NINGUN', 'ningunos': 'CUANT_NINGUN', 'ningunas': 'CUANT_NINGUN',
            'algunos': 'CUANT_ALGUNOS', 'algunas': 'CUANT_ALGUNOS', 'algun': 'CUANT_ALGUNOS', 'alguna': 'CUANT_ALGUNOS',
            'ciertos': 'CUANT_ALGUNOS', 'ciertas': 'CUANT_ALGUNOS', 'cierto': 'CUANT_ALGUNOS', 'cierta': 'CUANT_ALGUNOS'
        }
        
        # Relation and negation
        self.relation_verbs = {'es', 'son', 'fue', 'fueron', 'sera', 'seran', 'seria', 'serian', 'ha sido', 'han sido', 'habra sido'}
        self.negation_terms = {'no', 'ni', 'nunca', 'jamas', 'sin'}

        #Other relevant terms
        self.preserve={
            'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
            'y', 'o', 'ni', 'que', 'cual', 'cuyo', 'donde'
        }

        
        # Removes non-useful stopwords
        self.stopwords_es = set(stopwords.words('spanish'))
        self.stopwords_es -= self.negation_terms

        # Removes special characters
        self.no_special_chars = re.compile(r'[^\w\s]')
    
    def normalize_text(self, text):
        text = text.lower()
        text = ''.join(
            c for c in unicodedata.normalize('NFD', text)
            #Drops markers like accents
            if unicodedata.category(c) != 'Mn'
        )
        return self.no_special_chars.sub("", text)
    
    #Get subjet and predicate
    def extract_terms(self, text):
        # Applies normalization method and creates empty list of terms
        tokens = self.normalize_text(text).split()
        terms = []
        
        #Saves relevant terms
        for token in tokens:
            if token in self.quantifiers or token in self.relation_verbs or token in self.negation_terms:
                continue
            if token in self.stopwords_es and token not in self.preserve_terms:
                continue
            terms.append(token)
        
        return terms