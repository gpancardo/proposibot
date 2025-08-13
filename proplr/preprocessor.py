import unicodedata
from nltk.corpus import stopwords

class Preprocessor:
    def init(self):
        
        def __init__(self):
            # Cuantifiers
            self.quantifiers = {
                'todos': 'CUANT_TODO', 'todas': 'CUANT_TODO', 
                'ningún': 'CUANT_NINGUN', 'ninguna': 'CUANT_NINGUN',
                'algunos': 'CUANT_ALGUNOS', 'algunas': 'CUANT_ALGUNOS',
                'ciertos': 'CUANT_ALGUNOS', 'ciertas': 'CUANT_ALGUNOS'
            }
            
            #Relations and negations
            self.relation_verbs = {'es', 'son', 'fue', 'fueron','sera', 'seran', 'seria', 'serian','ha sido', 'han sido', 'habra sido'}
            self.negation_terms = {'no', 'ni', 'nunca', 'jamas', 'sin'}
            
            self.stopwords_es = set(stopwords.words('spanish'))
            self.stopwords_es -= {'no', 'ni'}
        
        
        def normalize_text(text):
            text = text.lower()
            text = ''.join(
                c for c in unicodedata.normalize('NFD', text)
                #Remove markers for accents
                if unicodedata.category(c) != 'Mn'
            )
            return text
        self.normalize_text = normalize_text