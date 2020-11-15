from nltk.corpus.reader.wordnet import Lemma
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import spacy
spacy.load("en_core_web_sm")
from spacy.lang.en import English
parser = English()

import pandas as pd
import csv
from csv import DictReader
import sys

##############################################################
##############################################################
##############################################################
##############################################################
# Part 1
##############################################################
##############################################################
##############################################################
##############################################################

##############################################################
##############################################################
# Creates a list of first names to be used later when removing
# unneccesary information
##############################################################
##############################################################

names = []

with open('fn_boys.csv') as allNames:
    name_dict = DictReader(allNames)

    for row in name_dict:
        names.append(row['FirstForename'].lower())
    
    print(len(names))
    
    print('Done with names')

with open('fn_girls.csv') as allNames:
    name_dict = DictReader(allNames)

    for row in name_dict:
        names.append(row['FirstForename'].lower())
    
    print(len(names))
    
    print('Done with names')

##############################################################
##############################################################
# Tokenizes a given script
##############################################################
##############################################################

def tokenize(script):
    listOfTokens = parser(script)
    ldaT = []

    for tk in listOfTokens:
        #print(tk)
        if tk.orth_.isspace():
            continue
        elif tk.like_url:
            ldaT.append('URL')
        elif tk.orth_.startswith('@'):
            ldaT.append('SCREEN_NAME')
        else:
            ldaT.append(tk.lower_)
    
    return ldaT

##############################################################
##############################################################
# Lemmatizes a given word
##############################################################
##############################################################

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

##############################################################
##############################################################
# Makes a list of stop words to be used for cleaning a given
# script
##############################################################
##############################################################

nltk.download('stopwords')
stopWords = set(nltk.corpus.stopwords.words('english'))

##############################################################
##############################################################
# This function sets up the script to be analyzed by the LDA
# model
##############################################################
##############################################################

def setUp(script):
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
# Part 2
##############################################################
##############################################################
##############################################################
##############################################################

##############################################################
##############################################################
# Reads the seinfeld scripts and does an initial clean of each
# episode then calls setUp to set up the script for analyzing.
# We then create a csv file storing each episode and it's
# now cleaned script.
##############################################################
##############################################################

counter = 0

episodeNumList = []
scriptList = []
scriptInfo = []

csv.field_size_limit(100000000)

with open('seinfeld_scripts.csv', 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)

    for row in csv_dict_reader:
        stop = False
        script2 = ""
        script3 = ""
        script4 = ""
        script5 = ""
        script6 = ""
        counterEnds = 0
        cleanedScript = ""

        for word in row['text'].split(' '):
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
            if len(word) > 0:# and "\n" not in word:
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

        scriptInfo.append(t)

        # if counter >= 50:
        #    break
    
    print('Done with Seinfeld Scripts')
    
    df = pd.DataFrame({
        'Episode Number': episodeNumList,
        'Script': scriptList})
    df.to_csv('cleanedSeinfeldScripts.csv', index=False)

##############################################################
##############################################################
# Reads the film scripts and does an initial clean of each
# movie then calls setUp to set up the script for analyzing.
##############################################################
##############################################################

filesForCorpus = []
counter  = 0

#with open('bunchOfScripts.csv', 'r') as read_obj:
with open('comedyScripts.csv', 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)

    for row in csv_dict_reader:
        stop = False
        script2 = ""
        script3 = ""
        script4 = ""
        script5 = ""
        script6 = ""
        counterEnds = 0
        cleanedScript = ""

        for word in row['Content'].split(' '):
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
            if len(word) > 0:# and "\n" not in word:
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

        t = setUp(cleanedScript)

        print(counter)

        filesForCorpus.append(t)

        # if counter >= 300:
        #     break

    print('Done with Film Scripts')

# with open('bunchOfScripts.csv') as manyAScript:
#     for aScript in manyAScript:
#         tks = setUp(aScript)
#         filesForCorpus.append(tks)

##############################################################
##############################################################
##############################################################
##############################################################
# Part 3
##############################################################
##############################################################
##############################################################
##############################################################

##############################################################
##############################################################
# Creates a corpus and a dictionary using the film scripts
##############################################################
##############################################################

AMT_OF_TOPICS = 10
AMT_OF_WORDS = 10

from gensim import corpora
dict = corpora.Dictionary(filesForCorpus)
dict.filter_extremes(no_below=40, no_above=0.75)
corp = [dict.doc2bow(script) for script in filesForCorpus]

import pickle
pickle.dump(corp, open('corpus.pkl', 'wb'))
dict.save('dictionary.gensim')

import gensim
ldamodel = gensim.models.ldamodel.LdaModel(corp, num_topics = 10, id2word = dict, passes = 2)
mod = 'model' + str(AMT_OF_TOPICS) + '.gensim'
ldamodel.save(mod)

##############################################################
##############################################################
# Here we take the Seinfeld scripts and analyze them using the
# LDA Model we created, finding the percentage of relevance
# between each script and the topics deduced from the corpus.
# We then use this information to create an overall topic
# model for the entire show.
##############################################################
##############################################################

topics = ldamodel.print_topics(num_words = AMT_OF_WORDS)
for topic in topics:
    print(topic)

epNum = 0 #to keep track of the amount of episodes
mostRelTopic = 0 #middle-man type variable
relTopicPerc = 0.0 #middle-man type vairable
totalPercTopics = [] #to store the average relevance of each topic in comparison to the entire show
percPerEpisode = [] #to store the average relevance of each topic in comparison to the each episode
mostRelTopicList = [] #to store the most relevant each topic in comparison to the each episode

#range is total number of topics. We initializing both arrays.
for i in range(10):
	totalPercTopics.append(0.0)
	percPerEpisode.append([])


for seinScript in scriptInfo:

    #runs the LDA Model on the given episode
    seinScript_bow = dict.doc2bow(seinScript)
    listOfRelTopics = ldamodel.get_document_topics(seinScript_bow)
    epNum += 1
    checkbox = 0

    #updates the lists with the information from the given episode
    for i in range(10):
        if len(listOfRelTopics) > checkbox:
            temp = listOfRelTopics[checkbox]
            if temp[0] == i:
                totalPercTopics[i] += temp[1]
                percPerEpisode[i].append(temp[1])
                if temp[1] > relTopicPerc:
                    mostRelTopic = i
                    relTopicPerc = temp[1]
                checkbox += 1
            else:
                percPerEpisode[i].append(0.002)
        else:
            percPerEpisode[i].append(0.002)
            totalPercTopics[i] += 0.002
        

    mostRelTopicList.append(mostRelTopic)
    mostRelTopic = 0
    relTopicPerc = 0.0

for i in range(AMT_OF_TOPICS):
    totalPercTopics[i] /= epNum

##############################################################
##############################################################
# Makes a csv file to store the information of each episode
# and the overall statistics of the show.
##############################################################
##############################################################

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

df2 = pd.DataFrame({
    'Topics': topics,
    'Average Relevance': totalPercTopics})

df2.to_csv('SeinfeldTopicAverage.csv', index=False)