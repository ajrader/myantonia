import re

#Function to turn character index into word index (note that it assumes there are only single spaces between words)
def index_changer(ind1,ind2,string):
    """
    ind1: the first character index
    ind2: the second character index
    string: the string that contains your word/phrase of interest
    """
    #string = string.replace("  ", " ")
    
    sum_word_lens=0
    split = string.split()
    indices=[]
    words=[]
    
    for indx,word in enumerate(split):
        
        if sum_word_lens >= ind1 and sum_word_lens < ind2:
            indices.extend([split.index(word,indx)])
            words.append(word)
        elif sum_word_lens > ind2:
            break
            
        sum_word_lens = sum_word_lens+len(word)+1 #Add 1 because of spaces trailing words   
    
    return indices,words

#Function to find the index of a word found from a regular expression in a string. Uses the index_changer function
def position_finder(method,text):
    """
    method: a compiled re object using the .finditer method. i.e. method=re.compile('^[0-9]').finditer(text)
    text: a string that you want to run the regular expression on
    """
    words = []
    positions = []
    
    for m in method:
        pos, wor = index_changer(m.start(),m.end(),text)
        positions.extend(pos)
        words.extend(wor)

    return positions,words

#Function to find "sensitive" words and their positions
def sensitive_info_finder(regex,text):
    """
    regex: a string that contains a regular expression to search for.
    text: a string that you want to search for a certain word/phrase in using regex
    """
    temp_regex = re.compile(regex)
    temp_found = temp_regex.finditer(text)
    
    temp_positions, temp_words = position_finder(temp_found,text)
    
    return temp_positions,temp_words

#Function to search for different types of sensitive information in a text
def regex_finder(text,return_categories=False):
    
    """
    text: a string that you wish to find "sensitive" information in
    return_categories: default False. If true function returns categories of sensitive information, and the information itself.
    """
    
    text = " ".join(text.split())
    #text = text.replace("  "," ")
    
    word_position_list = []
    word_label_list = []
    
    #Identify Credit Card numbers
    regex = "(?:3[47]\d{2}([\ \-]?)\d{6}([\ \-]?)\d|(?:(?:4\d|5[1-5]|65)\d{2}|6011)([\ \-]?)\d{4}([\ \-]?)\d{4}([\ \-]?))\d{4}"
    credit_card_positions, credit_card_words = sensitive_info_finder(regex,text)
    credit_card_tags = list(["Credit/Debit Card"])*len(credit_card_words)
    #print credit_card_words
    #print "=="
    
    #Identify e-mail addresses
    regex = "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}"
    email_positions, email_words = sensitive_info_finder(regex,text)
    email_tags = list(["Email"])*len(email_words)
    #print email_words
    #print "=="
    
    #Identify phone numbers
    regex = "(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}"
    phone_positions, phone_words = sensitive_info_finder(regex,text)
    phone_tags = list(["Phone Number"])*len(phone_words)
    #print phone_words
    #print "=="
    
    #Identify Social Security numbers
    regex = "(?!000)(?!666)(?!9)[X0-9]{3}([- ]?)(?!00)[X0-9]{2}([- ]?)(?!0000)\d{4}"
    ssn_positions, ssn_words = sensitive_info_finder(regex,text)
    ssn_tags = list(["SSN"])*len(ssn_words)
    #print ssn_words
    #print "=="
    
    #Identify birth date
    regex = """(?ix)             # case-insensitive, verbose regex
                   # match a word boundary
    (?:                   # match the following three times:
     (?:                  # either
      \d+                 # a number,
      (?:\.|st|nd|rd|th)* # followed by a dot, st, nd, rd, or th (optional)
      |                   # or a month name
      (?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*)
     )
     [\s./-]*             # followed by a date separator or whitespace (optional)
    ){3}                  # do this three times
                   # and end at a word boundary."""
    
    date_positions,date_words = sensitive_info_finder(regex,text)
    date_tags = list(["Date"])*len(date_words)
    #print date_words
    #print "=="
    
    #Identify income/financial information
    regex = "\$[0-9]*([,]?)[0-9]+"
    financial_positions, financial_words = sensitive_info_finder(regex,text)
    financial_tags = list(["Financial"])*len(financial_words)
    #print financial_words
    
    #There has to be a better way to do this last part..
    final_positions = credit_card_positions+email_positions+phone_positions+ssn_positions+date_positions+financial_positions
    final_words = credit_card_words+email_words+phone_words+ssn_words+date_words+financial_words
    final_tags = credit_card_tags+email_tags+phone_tags+ssn_tags+date_tags+financial_tags    
    
    if return_categories:
        return final_positions, final_tags, final_words
    else:
        return list(set(final_positions))