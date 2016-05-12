import hash_functions
import glob
import pandas as pd
import os

#files = glob.glob('frontend/Books/*.txt')
#with open( 'all_files.txt', 'w' ) as result:
#    for _ in files:
#        for line in open( _ , 'r' ):
#            result.write( line )
            
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

def get_words(filename, min_count, cache="all_text.pkl"):
    "Make a pd series of popular words"
    if cache:
        if os.path.exists(cache):
            series = pd.read_pickle(cache)
        else:
            series = pd.Series(word_count_dict(filename))
            series.to_pickle(cache)
    else:
        series = pd.Series(word_count_dict(filename))
    return series[series >= min_count]

def get_word_counts(text, words_series):
    results = []
    for word in text.split():
        word = hash_functions.clean(word)
        try:
            results.append(words_series[word])
        except KeyError:
            results.append(0)
    return results

def get_rare_word_positions(text, words_series):
    answers = get_word_counts(text, words_series)
    return [index for index, data in enumerate(answers) if data == 0]

if __name__ == "__main__":
    results = get_words("all_files.txt", 3)
    test_case = "William, whose cc number is 098170893741 is coming over to Jason's house who has a policy number aisod8f09a8oha and they will play Super Smash Bros. Kendall likes to write books. Milk is tasty. Mary likes Jack. We like Long and Hee and Smith and House"
    print zip(get_word_counts(test_case, results), test_case.split())