#!/usr/bin/env python
# coding: utf-8

from src.constants.numeric import *
import re

def string_from_numbers(text: str) -> list[int]:
    numbers = [int(s) for s in text.split() if s.isdigit()]
    return numbers


def number_in_words_2_numeric(text: str) -> int:
    # remove tudo o que não é alfanumérico
    clean_string = re.sub("[^0-9a-zA-Z\s]+", "", text)

    words = clean_string.upper().split()

    # verifica valores de 10 - 19
    for kt, vt in special_tens.items():
        if vt in words:
            return kt

    # verifica valores de 20 - 99
    for kt, vt in tens.items():
        if words.count(vt):
            position = words.index(vt)

            if words[position + 1] == "E":
                for ku, vu in units.items():
                    if words[position + 1:].count(vu):
                        return kt + ku
            return kt

    # verifica valores de 1 - 9
    for ku, vu in units.items():
        if words.count(vu):
            return ku

    return 0
