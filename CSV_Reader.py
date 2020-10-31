import pandas as pd
from csv import DictReader

#ourCSV = pd.read_csv('seinfeld_scripts.csv')

#firstScript = ourCSV["text"]

with open('seinfeld_scripts.csv', 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)
    for row in csv_dict_reader:
        print(row['text'])