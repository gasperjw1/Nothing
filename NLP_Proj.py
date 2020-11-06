#name, parentheses, and tags: clean up
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import html.parser
import unicodedata

BASE_URL = 'http://www.imsdb.com'
URL = 'http://www.imsdb.com/TV/Seinfeld.html'

r = urllib.request.urlopen(URL).read()
soup = BeautifulSoup(r, features="html.parser")

episodes = soup.findAll("p")

all_episodes = {'episode_num': [],
                'title': [],
                'air_date': [],
                'text': []}
episode_num = 0

# iterate through each episode
for episode in episodes:
    # get the URLs for each episode script and open that page
    episode_url = BASE_URL + episode.a['href']
    episode_page = urllib.request.urlopen(episode_url).read()
    episode_soup = BeautifulSoup(episode_page)

    # get link to script text and extract text
    script_details = episode_soup.findAll("table", class_="script-details")
    script_url = BASE_URL + script_details[0].findAll("a")[-1]["href"]
    script_page = urllib.request.urlopen(script_url).read()
    script_soup = BeautifulSoup(script_page)
    script = (script_soup
              .findAll("td", class_="scrtext")[0]
              .findAll("pre")[0]
              .getText)

    title = episode.a['title']
    script = str(script)
    episode_num += 1
    date = str(episode.a.next_sibling)[2:12]

    stop = False
    script2 = ""
    script3 = ""
    counterEnds = 0
    cleanedScript = ""

    for word in script:
        if word == "<\\b>":
            counterEnds  = counterEnds + 1
        if counterEnds >= 3:
            script2 = script2 + " " + word

    for word in script2:
        if word[0] == '(':
            stop = True
        
        if not stop:
            script3 = script3 + " " + word

        if word[len(word) - 1] == ')':
            stop = False
    
    stop = False

    for word in script3:
        if word == "<b>":
            stop = True
        
        if not stop:
            cleanedScript = cleanedScript + " " + word

        if word == "<\\b>":
            stop = False

    cleanedScript.replace("<b><\\b>","")

         
    all_episodes['episode_num'].append(episode_num)
    all_episodes['title'].append(title)
    all_episodes['air_date'].append(date)
    all_episodes['text'].append(cleanedScript)

    print("Episode " + str(episode_num) + "/176")

# seinfeld_df = pd.DataFrame(all_episodes)
# seinfeld_df.to_csv('seinfeld_scripts.csv', index_lable='episode_num')