import unicodedata
from nltk.corpus import stopwords
import re

class Preprocessor:
    def __init__(self):
        # Quantifiers dictionary
        self.quantifiers = {
            'todos': 'CUANT_TODO', 'todas': 'CUANT_TODO', 'todo': 'CUANT_TODO', 'toda': 'CUANT_TODO',
            'ningun': 'CUANT_NINGUN', 'ninguna': 'CUANT_NINGUN', 'ningunos': 'CUANT_NINGUN', 'ningunas': 'CUANT_NINGUN',
            'algunos': 'CUANT_ALGUNOS', 'algunas': 'CUANT_ALGUNOS', 'algun': 'CUANT_ALGUNOS', 'alguna': 'CUANT_ALGUNOS',
            'ciertos': 'CUANT_ALGUNOS', 'ciertas': 'CUANT_ALGUNOS', 'cierto': 'CUANT_ALGUNOS', 'cierta': 'CUANT_ALGUNOS'
        }
        
        # Relation verbs and negation terms
        self.relation_verbs = {'es', 'son', 'fue', 'fueron', 'sera', 'seran', 'seria', 'serian'}
        self.negation_terms = {'no', 'ni', 'nunca', 'jamas', 'sin'}

        # Other relevant terms to preserve during processing
        self.preserve_terms = {
            'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
            'y', 'o', 'ni', 'que', 'cual', 'cuyo', 'donde'
        }

        # Prepare stopwords list
        self.stopwords_es = set(self.normalize_text(word) for word in stopwords.words('spanish'))
        # Remove negation terms from stopwords since they're handled separately
        self.stopwords_es -= self.negation_terms

        # Regex pattern to remove special characters
        self.no_special_chars = re.compile(r'[^\w\s]')
    
    def normalize_text(self, text):
        text = text.lower()
        # Remove diacritical marks (accents) while preserving base characters
        text = ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'  # Mn: Nonspacing Mark
        )
        # Remove any remaining special characters
        return self.no_special_chars.sub("", text)
    
    def extract_terms(self, text):
        # Normalize and tokenize the input text
        tokens = self.normalize_text(text).split()
        terms = []
        
        # Process each token to identify relevant terms
        for token in tokens:
            # Skip quantifiers, relation verbs, and negation terms
            if token in self.quantifiers or token in self.relation_verbs or token in self.negation_terms:
                continue
            # Skip regular stopwords but preserve important terms
            if token in self.stopwords_es and token not in self.preserve_terms:
                continue
            terms.append(token)
        
        return terms
    
    def preprocess(self, text):
        text = self.normalize_text(text)
        tokens = text.split()
        processed_tokens = []
        negation_detected = False
        
        # Process each token to create normalized representation
        for token in tokens:
            # Handle negation terms (set flag but don't add to output)
            if token in self.negation_terms:
                negation_detected = True
                continue
            # Replace quantifiers with their category tags
            if token in self.quantifiers:
                processed_tokens.append(self.quantifiers[token])
                continue
            # Replace relation verbs with generic tag
            if token in self.relation_verbs:
                processed_tokens.append('VERBO_RELACION')
                continue
            # Preserve important terms
            if token in self.preserve_terms:
                processed_tokens.append(token)
                continue
            # Skip regular stopwords
            if token in self.stopwords_es:
                continue
            # All other terms get generic "TERMINO" tag
            processed_tokens.append('TERMINO')
        
        # Add negation marker at end if any negation was detected
        if negation_detected:
            processed_tokens.append('NEGACION')
            
        return " ".join(processed_tokens)