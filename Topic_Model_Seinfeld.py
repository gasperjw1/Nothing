import spacy
spacy.load("en_core_web_sm")
from spacy.lang.en import English
parser = English()

def tokenize(script):
    listOfTokens = parser(script)
    ldaT = []

    for tk in listOfTokens:
        if tk.orth_.isspace():
            continue
        elif tk.like_url:
            ldaT.append('URL')
        elif tk.orth_.startswith('@'):
            ldaT.append('SCREEN_NAME')
        else:
            ldaT.append(tk.lower_)
    
    return ldaT

import nltk