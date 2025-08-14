import unittest

class TestPreprocessor(unittest.TestCase):
    def setUp(self):
        from preprocessor import Preprocessor  # Ajusta el nombre del archivo
        self.preprocessor = Preprocessor()
        # Lista de palabras preservadas que queremos ignorar en el test
        self.preservadas = {'el', 'la', 'los', 'las', 'un', 'una', 'y', 'o', 'de', 'del', 'en'}

    def clean_output(self, text):
        # Normaliza y quita las preservadas para comparar resultados
        tokens = text.split()
        return [t for t in tokens if t not in self.preservadas]

    def test_preprocess_ignora_preservadas(self):
        entrada = "Todos los gatos no son blancos y algunas casas son grandes"
        salida_esperada = ['CUANT_TODO', 'NEGACION', 'VERBO_RELACION', 'TERMINO', 'CUANT_ALGUNOS', 'VERBO_RELACION', 'TERMINO']
        
        procesado = self.clean_output(self.preprocessor.preprocess(entrada))
        self.assertEqual(procesado, salida_esperada)

if __name__ == '__main__':
    unittest.main()
