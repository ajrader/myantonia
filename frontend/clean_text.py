from hash_functions import hash_term

class CleanData():
    def __init__(self, name_function=None, regex_function=None, rare_word_function=None,
                 name_corpus=None, book_corpus=None, method="any", spell_check=False):
        """
        Single interface to clean text
        """
        # Compile REGEX functions here
        self.method = method
        self.spell_check = spell_check
        self.name_corpus = name_corpus
        self.name_function = name_function
        self.regex_function = regex_function
        self.book_corpus = book_corpus
        self.rare_word_function = rare_word_function

    def suspicious_word_locations(self, text):
        results = []
        results.extend(self.name_function(text, self.name_corpus))
        results.extend(self.regex_function(text))
        results.extend(self.rare_word_function(text, self.book_corpus))
        #for function in self.functions:
        #    results.extend(function(text))
        if self.method == "any":
            results = list(set(results))
        return results
    
    def anonymized_text(self, text):
        final_words = []
        term_locations = self.suspicious_word_locations(text)
        for index, word in enumerate(text.split()):
            punctuation_at_end = False
            if index in term_locations:
                last_character = word[-1]
                if last_character in '!"%&\),./:;>?]}':
                    word = word[:-1]
                    punctuation_at_end = True
                word_length = len(word)
                word = hash_term(word)[:word_length]
            if punctuation_at_end:
                word += last_character
            final_words.append(word)
        return " ".join(final_words)