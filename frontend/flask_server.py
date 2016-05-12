from flask import Flask, abort, jsonify, request, send_from_directory
from flask_cors import CORS
import clean_text
import hash_functions
import name_finder
import regex_function_working
import get_rare_words

name_corpus = name_finder.load_names()
results = get_rare_words.get_words("all_files.txt", 3)

clean_data = clean_text.CleanData(name_function=name_finder.name_positions,
                                  regex_function=regex_function_working.regex_finder,
                                  rare_word_function=get_rare_words.get_rare_word_positions,
                                  book_corpus=results,
                                  name_corpus=name_corpus)
                                  

app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def index():
    return "Flask Server Life Event Service"

@app.route('/anon', methods = ['POST'])
def handle_client():
    #this be the input data structure
    data = request.get_data()
    
    data = clean_data.anonymized_text(data)

    return data

    
if __name__ == '__main__':
    app.run(port=8080, debug=True, host='127.0.0.1')    
