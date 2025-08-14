import unittest
from preprocessor import Preprocessor

class TestPreprocessor(unittest.TestCase):
    def setUp(self):
        self.preprocessor = Preprocessor()
    
    def test_normalize_text(self):
        self.assertEqual(self.preprocessor.normalize_text("HOLÁ"), "hola")
        self.assertEqual(self.preprocessor.normalize_text("café"), "cafe")
        self.assertEqual(self.preprocessor.normalize_text("hello! world?"), "hello world")
        self.assertEqual(self.preprocessor.normalize_text("¿Qué Tal?"), "que tal")
    
    def test_extract_terms(self):
        # Test stopword removal (excluding negation terms)
        text = "el gato y el perro no juegan"
        self.assertEqual(self.preprocessor.extract_terms(text), ["gato", "perro", "no", "juegan"])
        
        # Test negation terms are preserved
        text = "nunca voy sin permiso"
        self.assertEqual(self.preprocessor.extract_terms(text), ["nunca", "voy", "sin", "permiso"])
        
        # Test normalization during extraction
        text = "Los ÁRBOLES verdes"
        self.assertEqual(self.preprocessor.extract_terms(text), ["arboles", "verdes"])
    
    def test_preprocess(self):
        # Test quantifier replacement
        text = "todos los gatos y algunas perros"
        expected = "CUANT_TODO TERMINO CUANT_ALGUNOS TERMINO"
        self.assertEqual(self.preprocessor.preprocess(text), expected)
        
        # Test relation verb replacement - FIXED: "ellos" and "ella" are stopwords
        text = "ellos son amigos y ella es doctora"
        expected = "VERBO_RELACION TERMINO VERBO_RELACION TERMINO"
        self.assertEqual(self.preprocessor.preprocess(text), expected)
        
        # Test negation handling - FIXED: "hay" and "nada" are stopwords
        text = "no hay nada ni nunca volverá"
        expected = "NEGACION NEGACION NEGACION TERMINO"
        self.assertEqual(self.preprocessor.preprocess(text), expected)
        
        # Test stopword removal and term preservation
        text = "el cielo es azul"
        expected = "TERMINO VERBO_RELACION TERMINO"
        self.assertEqual(self.preprocessor.preprocess(text), expected)
        
        # Test combined operations
        text = "¡Ningún niño debe comer! ¿Cierto?"
        expected = "CUANT_NINGUN TERMINO TERMINO TERMINO CUANT_ALGUNOS"
        self.assertEqual(self.preprocessor.preprocess(text), expected)

if __name__ == '__main__':
    unittest.main()