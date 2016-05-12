import hash_functions
import pandas as pd

def load_names():
    #Last names
    last_names = pd.read_fwf('Names/dist.all.last', header=None, widths=[14,7,7,7])
    first_male = pd.read_fwf('Names/dist.male.first', header=None, widths=[14,7,7,7])
    first_female = pd.read_fwf('Names/dist.female.first', header=None, widths=[14,7,7,7])
    subset_last_name = last_names[last_names[2]<=70]
    subset_first_male = first_male[first_male[2]<=80]
    subset_first_femal = first_female[first_female[2]<=80]
    names = pd.concat([subset_last_name[0], subset_first_male[0], subset_first_femal[0]], ignore_index=True)
    return names

def is_name(name, name_corpus):
    return hash_functions.clean(name).upper() in name_corpus.values

def capital_words(text):
    results = []
    for words in text.split():
        if words[0].isupper():
            results.append(words)
    return results

def name_positions(text, name_corpus):
    results = []
    for index, name in enumerate(text.split()):
        if name[0].isupper() and is_name(name, name_corpus):
            results.append(index)
    return results

if __name__ == "__main__":
    names = load_names()
    test_case = "William is coming over to Jason's house and they will play Super Smash Bros. Kendall likes to write books. Milk is tasty. Mary likes Jack. We like Long and Hee and Smith and House"
    print name_positions(test_case)