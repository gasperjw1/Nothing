from nltk.corpus.reader.wordnet import Lemma
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
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
def getLemma(word):
    lem = wn.morphy(word)
    if lem is None:
        return word
    else:
        return lem

from nltk.stem.wordnet import WordNetLemmatizer
def getLemma2(word):
    return WordNetLemmatizer().lemmatize(word)

nltk.download('stopwords')
stopWords = set(nltk.corpus.stopwords.words('english'))

def setUp(script):
    names = ['jerry', 'kramer', 'george', 'elaine', 'larry', 'david', 'newman', 'pensky']
    tokens = tokenize(script)
    tokens = [tk for tk in tokens if len(tk) > 4]
    tokens = [tk for tk in tokens if tk not in stopWords]
    tokens = [tk for tk in tokens if tk not in names]
    tokens = [getLemma(tk) for tk in tokens]

    return tokens


##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################

import pandas as pd
import csv
from csv import DictReader
import sys

#ourCSV = pd.read_csv('seinfeld_scripts.csv')

#firstScript = ourCSV["text"]

counter = 0

episodeNumList = []
scriptList = []
scriptInfo = []

csv.field_size_limit(100000000)

with open('seinfeld_scripts.csv', 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)

    for row in csv_dict_reader:
        #print(row['text'])

        stop = False
        script2 = ""
        script3 = ""
        script4 = ""
        script5 = ""
        script6 = ""
        counterEnds = 0
        cleanedScript = ""

        #print(row['text'])

        for word in row['text'].split(' '):
            #print(word)
            #if "</b>" in word:
            #    print(word)
            #    counterEnds  = counterEnds + 1
            #if counterEnds >= 3:
            #    script2 = script2 + " " + word

            if "<" not in word:
                script2 = script2 + ' ' + word
        
        #print(script2)

        for word in script2.split(' '):
            if '(' in word:
                stop = True
            
            if not stop:
                script3 = script3 + " " + word

            if ')' in word:
                stop = False
        
        #print(script3)
        
        stop = False

        #for word in script3:
        #    if word == "<b>":
        #        stop = True
            
        #    if not stop:
        #        cleanedScript = cleanedScript + " " + word

        #    if word == "<\\b>":
        #        stop = False

        #cleanedScript.replace("<b><\\b>","")

        for word in script3.split(' '):
            #print(word)
            if len(word) > 0 and "\n" not in word:
                script4 = script4 + " " + word

        #print(script4)

        for word in script4.split(' '):
            tempWord = ""
            for letter in word:
                if letter == "." or letter == "!" or letter == "?":
                    tempWord = tempWord + " "
                else:
                    tempWord = tempWord + letter

            cleanedScript = cleanedScript + " " + tempWord

        #print(cleanedScript)
        #print("------------------------------------------------------------------")

        counter += 1

        # episodeNumList.append(counter)
        # scriptList.append(cleanedScript)

        t = setUp(cleanedScript)

        # if counter % 20 == 0:
        #     print(t)

        scriptInfo.append(t)

        #if counter >= 170:
        #    break
                
        #break
    
    # df = pd.DataFrame({
    #     'Episode Number': episodeNumList,
    #     'Script': scriptList,
    #     'Tokens': scriptInfo})
    # df.to_csv('out2.csv', index=False)

##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################

from gensim import corpora
dict = corpora.Dictionary(scriptInfo)
corp = [dict.doc2bow(script) for script in scriptInfo]

import pickle
pickle.dump(corp, open('corpus.pkl', 'wb'))
dict.save('dictionary.gensim')

import gensim
ldamodel = gensim.models.ldamodel.LdaModel(corp, num_topics = 10, id2word = dict, passes = 15)
ldamodel.save('model10.gensim')

topics = ldamodel.print_topics(num_words=4)
for topic in topics:
    print(topic)

