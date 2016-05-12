import os
import glob
import hash_functions
import numpy as np
import pandas as pd
import re

dirname = "Books/"

files = glob.glob(dirname+'*.txt')
with open('all_files.txt', 'w') as result:
    for _ in files:
        for line in open( _ , 'r' ):
            result.write( line )


def word_count_dict(filename):
    word_count = {}
    input_file = open(filename, 'r')
    for line in input_file:
        words = line.split(" ")
        for word in words:
            word = hash_functions.clean(word)
            word = word.strip()
            if word == '':
                continue
            word_count.setdefault(word,0)
            word_count[word]+=1
    input_file.close()
    return word_count


def get_words(filename, min_count):
    series = pd.Series(word_count_dict(filename))
    return series[series >= min_count]


class GenerateData(object):
    def __init__(self, dict_file_name, eng_names_file_name):
        self.dict_file_name = dict_file_name
        self.eng_names_file_name = eng_names_file_name
    
    def word_count_dict(self):
        word_count = {}
        input_file = open(self.dict_file_name, 'r')
        for line in input_file:
            words = line.split(" ")
            for word in words:
                word = hash_functions.clean(word)
                word = word.strip()
                if word == '':
                    continue
                word_count.setdefault(word,0)
                word_count[word]+=1
        input_file.close()
        return word_count
    
    def get_words_from_dict(self, min_count):
        words_series = pd.Series(self.word_count_dict())
        return words_series[words_series >= min_count]
    
    def get_names(self):
        eng_names = pd.read_csv(self.eng_names_file_name, header=False)
        eng_names = list(eng_names.names)
        eng_names = [name.lower() for name in eng_names]
        return eng_names


generate_data = GenerateData(dict_file_name = 'all_files.txt', eng_names_file_name = 'name_list.csv')
words_from_dict = generate_data.get_words_from_dict(3)
english_names = generate_data.get_names()


class Test(object):
    def __init__(self, text, sensetive_words = None, list_of_indices = None, temp = None):
        self.text = hash_functions.clean(text).lower()
        self.sensetive_words = None
        self.list_of_indices = None
        self.temp = None
        
    def get_sensetive_words(self, words_from_dict):
        words = self.text.split(" ")
        counts = pd.Series([words_from_dict.get(word, default=0) for word in words], index=words)
        self.sensetive_words = list(counts[counts<2].index)
    
    def get_indices_english_names(self, english_names):
        self.temp = []
        count = 0
        
        for name in self.text.split(" "):
            count = count+1
            if name in (english_names + self.sensetive_words):
                self.temp.append(count-1)


test_text = "David Hello! My name is jeff myer David $Jeff Jason Sanchez and my phone number is 928-899-5248"


def implement(test_text):
    test = Test(test_text)
    test.get_sensetive_words(words_from_dict)
    test.get_indices_english_names(english_names)
    return test.temp



