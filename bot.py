#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys;
import hashlib;
import time;
import tweepy;
import subprocess
from  twitterAuth import *;

#INIT tweepy
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
#URL for finansinspektionen
url = "https://marknadssok.fi.se"


file_name = 'insyn.txt'
current_data_tweet = file_name.encode("utf8")

while True:
    scrape = subprocess.call("./fin.sh")
    with open(file_name) as file_to_check:
        # read contents of the file
        new_data_tweet = file_to_check.read().encode("utf8")
        #Check if there are any updates
        if hashlib.md5(current_data_tweet).hexdigest() != hashlib.md5(new_data_tweet).hexdigest():
            current_data_tweet = new_data_tweet
            with open(file_name) as f:
                td = [line.rstrip('\n') for line in f]
                #uggly tweet string
                tweet =  "[" + td[9] + "]|[" + td[0] + "]: " + td[2] + " " + td[1] + " Rapporterar " + td[3] + " av " + td[4] + " [" + td[5] +"]@["+ td[7]+td[8]+"]. Läs mer här: " + url + td[10]
            api.update_status(status=tweet)        
            print (tweet)

        else:
            print("Inget nytt Insiderköp")
            time.sleep(5)
