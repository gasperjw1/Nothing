import pandas as pd
import csv
from csv import DictReader
import sys

#ourCSV = pd.read_csv('seinfeld_scripts.csv')

#firstScript = ourCSV["text"]

counter = 0

episodeNumList = []
scriptList = []

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

        #if counter >= 170:
        #    break
                
        #break
    
    df = pd.DataFrame({
        'Episode Number': episodeNumList,
        'Script': scriptList})
    df.to_csv('out.csv', index=False)