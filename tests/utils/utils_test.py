#!/usr/bin/env python
# coding: utf-8

import unittest
from src.utils.utils import number_in_words_2_numeric

class MultiplyTestCase(unittest.TestCase):

    def test_number_unit_start(self):
        result = number_in_words_2_numeric("Oito palavras? Fé, Amor, generosidade, perdão, família, gentileza, resiliência e chocolate.")
        self.assertEqual(result, 8)
       
    def test_number_unit_mid(self):
        result = number_in_words_2_numeric("Uma semana tem sete dias")
        self.assertEqual(result, 7)
       
    def test_number_unit_end(self):
        result = number_in_words_2_numeric("Eu sou jogador número um")
        self.assertEqual(result, 1)
        
    def test_number_tens_start(self):
        result = number_in_words_2_numeric("Vinte contar um segredo!")
        self.assertEqual(result, 20)
       
    def test_number_tens_mid(self):
        result = number_in_words_2_numeric("Um mês tem trinta dias")
        self.assertEqual(result, 30)
       
    def test_number_tens_end(self):
        result = number_in_words_2_numeric("Ontem assisti Super Onze")
        self.assertEqual(result, 11)
    
    def test_number_complete(self):
        result = number_in_words_2_numeric("Oitenta e um anos")
        self.assertEqual(result, 81)

    def test_number_first_check(self):
        result = number_in_words_2_numeric("Oitenta e muitos")
        self.assertEqual(result, 80)
        
    def test_number_many_numbers(self):
        result = number_in_words_2_numeric("Um, dois, três, quatro...")
        self.assertEqual(result, 1)
        
    def test_no_numbers(self):
        result = number_in_words_2_numeric("Não existe nenhum número aqui")
        self.assertEqual(result, 0)
        
if __name__ == '__main__':
    unittest.main()
    