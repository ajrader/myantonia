from hashlib import sha1

def clean(s):
    "Removes punctuation and converts to lower case. Does not remove spaces"
    return s.encode('string-escape').replace("\\n", " ").translate(None, '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~').lower()

def hash_term(term, pepper="A super secret complex sentence that is very hard to guess"):
    "Cleans the term, adds the pepper, and returns the hashed result"
    return sha1(clean(term) + pepper).hexdigest()

if __name__ == "__main__":
    # Test cases
    assert(clean("CAT,") == "cat")
    assert(clean("schweizerk\xc3\xa4se") == 'schweizerkxc3xa4se')
    assert(clean("Wow! That's neat-o") == 'wow thats neato')