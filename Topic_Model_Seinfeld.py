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
    #names = ['jerry', 'kramer', 'george', 'elaine', 'larry', 'david', 'newman', 'pensky']
    tokens = tokenize(script)
    tokens = [tk for tk in tokens if len(tk) > 4]
    tokens = [tk for tk in tokens if tk not in stopWords]
    #tokens = [tk for tk in tokens if tk not in names]
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

        episodeNumList.append(counter)
        scriptList.append(cleanedScript)

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

filesForCorpus = []
counter  = 0

with open('bunchOfScripts.csv', 'r') as read_obj:
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

        for word in row['Content'].split(' '):
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

        for word in script3.split(' '):
            #print(word)
            if len(word) > 0 and "\n" not in word:
                script4 = script4 + " " + word


        for word in script4.split(' '):
            tempWord = ""
            for letter in word:
                if letter == "." or letter == "!" or letter == "?":
                    tempWord = tempWord + " "
                else:
                    tempWord = tempWord + letter

            cleanedScript = cleanedScript + " " + tempWord

        counter += 1

        # episodeNumList.append(counter)
        # scriptList.append(cleanedScript)

        t = setUp(cleanedScript)

        print(counter)

        filesForCorpus.append(t)

        if counter >= 300:
            break

# with open('bunchOfScripts.csv') as manyAScript:
#     for aScript in manyAScript:
#         tks = setUp(aScript)
#         filesForCorpus.append(tks)

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

AMT_OF_TOPICS = 10
AMT_OF_WORDS = 10

from gensim import corpora
dict = corpora.Dictionary(filesForCorpus)
dict.filter_extremes(no_below=40, no_above=0.5, keep_n=1500)
corp = [dict.doc2bow(script) for script in filesForCorpus]

import pickle
pickle.dump(corp, open('corpus.pkl', 'wb'))
dict.save('dictionary.gensim')

import gensim
#from gensim.models import LdaMulticore
ldamodel = gensim.models.ldamodel.LdaModel(corp, num_topics = 10, id2word = dict, passes = 2)
#ldamodel = LdaMulticore(corp, id2word=dict, passes=2, workers=2, num_topics= AMT_OF_TOPICS)
ldamodel.save('model10.gensim')

##############################################################
##############################################################
##############################################################
##############################################################
##############################################################

topics = ldamodel.print_topics(num_words = 10)
for topic in topics:
    print(topic)

epNum = 0
mostRelTopic = 0
relTopicPerc = 0.0
temp = 0.0
totalPercTopics = []
percPerEpisode = []
mostRelTopicList = []

#range is total number of topics. We initializing both arrays.
for i in range(10):
	totalPercTopics.append(0.0)
	percPerEpisode.append([])


for seinScript in scriptInfo:
	seinScript_bow = dict.doc2bow(seinScript)
	listOfRelTopics = ldamodel.get_document_topics(seinScript_bow)

	epNum += 1

	# for i in listOfRelTopics:
	# 	totalPercTopics[i[0]] += i[1]
	# 	percPerEpisode[i[0]].append(i[1])

	# 	if temp > relTopicPerc:
	# 		mostRelTopic = i[0]
	# 		relTopicPerc = i[1]
        

	mostRelTopicList.append(mostRelTopic)
	mostRelTopic = 0
	relTopicPerc = 0.0

for i in range(AMT_OF_TOPICS):
    t = True
    totalPercTopics[i] /= epNum

print('The average topic relation: ')
print(totalPercTopics)

#Needs to be updated when AMT_OF_TOPICS is changed
df = pd.DataFrame({
	'Episode Number': episodeNumList,
	'Script': scriptList,
	'Main Topic': mostRelTopicList,
	'Topic 1 Relevance': percPerEpisode[0],
	'Topic 2 Relevance': percPerEpisode[1],
	'Topic 3 Relevance': percPerEpisode[2],
	'Topic 4 Relevance': percPerEpisode[3],
	'Topic 5 Relevance': percPerEpisode[4],
	'Topic 6 Relevance': percPerEpisode[5],
	'Topic 7 Relevance': percPerEpisode[6],
	'Topic 8 Relevance': percPerEpisode[7],
	'Topic 9 Relevance': percPerEpisode[8],
	'Topic 10 Relevance': percPerEpisode[9]})

df.to_csv('SeinfeldTopicModel.csv', index=False)


# df2 = pd.DataFrame({
#	'Number': [1,2,3,4,5,6,7,8,9,10],
#	'Topic': topics})
#
# df2.to_csv('ListOfTopics.csv', index=False)