from contextlib import closing
from bs4 import BeautifulSoup
from sim import simple_get
import sys
import hashlib
import time
import math
import tweepy
from os import environ, error


auth = tweepy.OAuthHandler(environ["CONSUMER_KEY"], environ["CONSUMER_SECRET"])
auth.set_access_token(environ["ACCESS_KEY"], environ["ACCESS_SECRET"])
api = tweepy.API(auth)
def makeTweet(tweet):
    #tweet[]
    
    stringbuilder = ""
    close = ""
    if tweet["Närstående"] == "Ja":
        close = "Närstående till "
    try:
        total = (float(tweet["Pris"].replace(',','.'))*int(tweet["Volym"]))
        total = "{:0,.2f}".format(float(total))
    except ValueError:
        total = tweet["Pris"]*tweet["Volym"]

    stringbuilder = ( "[" + tweet["Utgivare"] + "] " + close +
        tweet["Befattning"]  + " "+ tweet["Person i ledande ställning"] +
        " rapporterar " + tweet["Karaktär"].lower() + " av " + tweet["Instrumentnamn"] + "[" +
        tweet["Volym"] + "]@[" + tweet["Pris"] + "] Totalt: " +
            total + " " +  tweet["Valuta"] +
        ".  Läs mer här: https://marknadssok.fi.se" + tweet["Detaljer"])

    
        
    

    print(stringbuilder)
    try:
        api.update_status(status=stringbuilder)
        print(stringbuilder)
    except tweepy.error.TweepError :
        print('error:')
    else:
        print("Tweetad")

def tweet():
    lasttweet = {}
    while True:
        datasets = getData(lasttweet)
        if len(datasets) > 0:
            for a in datasets:
                makeTweet(a)

            lasttweet = datasets[-1]
            time.sleep(10)
        else:
            print("Fick ingen DATA")
            time.sleep(10)


def getData(lasttweet):
    datasets = []

    #URL till listan på fi.se
    url = ("https://marknadssok.fi.se/publiceringsklient/?Page=1")
    raw_html = simple_get(url)
    soup = BeautifulSoup(raw_html, 'html.parser')

    #Find Table
    table = soup.find("table", attrs={"class":"table"})
    #Find head
    head = [th.get_text() for th in table.find("tr").find_all("th")]
    head = [w.replace('\n', 'Detaljer') for w in head]
    #for row in table.find_all("tr")[1:]:
    datasets = [dict(zip(head,[td.get_text() if not td.a else td.a['href'] for td in row.find_all("td")])) for row in table.find_all('tr')[1:]]
    #datasets.append(dataset)
    datasets.reverse()


    index = 0
    #Check if last tweet
    for j in range(0,len(datasets)):
        if hashlib.md5(''.join(datasets[j].values()).encode("utf8")).hexdigest() == hashlib.md5(''.join(lasttweet.values()).encode("utf8")).hexdigest():
            index = j
            print (index)
            if index == 0:
                return []
            return datasets[j+1:]


    print("Hittade INTE last tweet")
    return datasets
tweet()
