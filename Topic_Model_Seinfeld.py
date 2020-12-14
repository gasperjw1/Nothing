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

with open('./initialInformation/fn_boys.csv') as allNames:
    name_dict = DictReader(allNames)

    for row in name_dict:
        names.append(row['FirstForename'].lower())
    
    print(len(names))
    
    print('Done with names')

with open('./initialInformation/fn_girls.csv') as allNames:
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

from nltk import word_tokenize, pos_tag
nltk.download('averaged_perceptron_tagger')


def setUp(script):

    is_noun_adj = lambda pos: pos[:2] == 'NN' or pos[:2] == 'JJ'

    tokens = tokenize(script)
    tokens = [tk for tk in tokens if len(tk) > 4]
    tokens = [tk for tk in tokens if tk not in stopWords]
    tokens = [tk for tk in tokens if tk not in names and tk != 'fuckin']
    tokens = [tk for (tk, pos) in pos_tag(tokens) if is_noun_adj(pos)]
    tokens = [getLemma2(tk) for tk in tokens]

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

with open('./initialInformation/seinfeld_scripts.csv', 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)

    for row in csv_dict_reader:
        stop = False
        script2 = ""
        script3 = ""
        script4 = ""
        cleanedScript = ""

        for word in row['text'].split(' '):
            if "<" not in word:
                script2 = script2 + ' ' + word

        for word in script2.split(' '):
            if '(' in word:
                stop = True
            
            if not stop:
                script3 = script3 + " " + word

            if ')' in word:
                stop = False
        
        stop = False

        for word in script3.split(' '):
            if len(word) > 0:
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

        episodeNumList.append(counter)
        scriptList.append(cleanedScript)

        t = setUp(cleanedScript)

        scriptInfo.append(t)
    
    print('Done with Seinfeld Scripts')
    
    df = pd.DataFrame({
        'Episode Number': episodeNumList,
        'Script': scriptList})
    df.to_csv('results/cleanedSeinfeldScripts.csv', index=False)

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
# Creates a corpus and a dictionary using the Bag-of-Words
##############################################################
##############################################################

comedy = ['hilarious', 'enjoy', 'fun', 'crazy','absurd', 'ironic', 'laugh', 'funny', 'ridiculous']
romance = ['relationship', 'marriage', 'like', 'admire', 'passion', 'love', 'connection', 'communication', 'divorce']
drama = ['intense', 'serious',  'sad',  'conflict', 'life', 'death', 'pain', 'mad', 'cry']
childrens = ['cartoon', 'fantasy', 'adventure', 'corny', 'light', 'educational', 'family', 'school', 'friendship']
family = ['brother', 'sister', 'father', 'mother', 'relationship', 'love', 'friend', 'family']
mystery = ['clue', 'murder', 'detective', 'weapon', 'doubt', 'investigation', 'alibi', 'motive', 'victim']

bagOfWords = [comedy,romance,drama,childrens,family,mystery]

AMT_OF_TOPICS = 6
AMT_OF_WORDS = 9

from gensim import corpora
dict = corpora.Dictionary( bagOfWords )
corp = [dict.doc2bow(genre) for genre in bagOfWords]

import pickle
pickle.dump(corp, open('corpus.pkl', 'wb'))
dict.save('dictionary.gensim')

import gensim
ldamodel = gensim.models.ldamodel.LdaModel(corp, num_topics = AMT_OF_TOPICS, id2word = dict, passes = 10)
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

# Range is total number of topics. We initializing both arrays.
for i in range(AMT_OF_TOPICS):
	totalPercTopics.append(0.0)
	percPerEpisode.append([])


for seinScript in scriptInfo:

    # Runs the LDA Model on the given episode
    seinScript_bow = dict.doc2bow(seinScript)
    listOfRelTopics = ldamodel.get_document_topics(seinScript_bow)
    epNum += 1
    checkbox = 0

    # Updates the lists with the information from the given episode
    for i in range(AMT_OF_TOPICS):
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
        

    mostRelTopicList.append((mostRelTopic + 1))
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

df = pd.DataFrame({
	'Episode Number': episodeNumList,
	'Main Topic': mostRelTopicList
    })

topicNum = 0
for top in percPerEpisode:
    columnName = 'Topic ' + str(topicNum + 1) + ' Relevance'
    df[columnName] = top
    topicNum += 1
 
df.to_csv('results/SeinfeldTopicModel.csv', index=False)

df2 = pd.DataFrame({
    'Topics': topics,
    'Average Relevance': totalPercTopics})

df2.to_csv('results/SeinfeldTopicAverage.csv', index=False)