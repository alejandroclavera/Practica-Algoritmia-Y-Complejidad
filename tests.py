'''
Module in charge of doing the tests.
'''
import unittest
import preprocesamiento
import alineamiento
def get_format(lengths):
    '''Creates structure for the function calculate_median'''
    formated = []
    for length in lengths:
        formated.append(('', length))
    return formated
class TestSarcovhierachy(unittest.TestCase):
    '''Test Class'''
    def test_preprocessing(self):
        '''Test preprocessing'''
        print('-------Test Preprocesamiento-------')
        test_a = get_format([
            3232323, 23213213, 5533544, 778, 1, 56, 75, 999, 0, 43, 23, 4444444, 32])
        test_b = get_format([333, 57, 224, 54, 56, 78, 9, 10])
        self.assertEqual(preprocesamiento.calculate_median(test_a)[1], 75)
        self.assertEqual(preprocesamiento.calculate_median(test_b)[1], 57)
        print('Correcto')

    def test_alignment(self):
        '''Test Alignment.'''
        print('-------Test Alineamiento-------')
        sample_a = 'AGGT'
        sample_b = 'AGTTA'
        sample_c = 'AAAAGTTTTCCC'
        sample_d = 'TTGCCCA'
        self.assertEqual(alineamiento.calc_needleman_score(sample_a, sample_b, max_len=10), 5)
        self.assertEqual(alineamiento.calc_needleman_score(sample_c, sample_d, max_len=20), -5)
        print('Correcto')
if __name__ == '__main__':
    unittest.main()
