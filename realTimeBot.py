#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on Dec 5, 2013

@author: Benjamin
'''

import tweepy
import sys
import time
import Classifier
import Analysis
import readDictionary
import datetime

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="Iojc087MRYfTa5d94STA"
consumer_secret="lcXr7l7bi0Jr91wmIkLtWnyZQsiJu82CkiXobLrmA"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located 
# under "Your access token")
access_token="2215049539-7KIgG3CnqvrTOCUhlYfHeGVQTkwvZPHbJpMDZas"
access_token_secret="JStIVe2M3lVWr02pOpHjYJJEInYwmBSdq7ig83jwJ9YF3"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
        
    def __init__(self, clf, analyzer, emoticons, api):
        self.clf = clf
        self.analyzer = analyzer
        self.emoticons = emoticons
        tweepy.StreamListener.__init__(self)
        self.api = api
        self.t0 = time.time() 
        output = open('tweets/' + str(self.t0), 'w')
        output.close()
        self.count = 0
        
    def on_status(self, status):
        if status.lang == "en":
            output = open('tweets/' + str(self.t0), 'a')
            text = status.text.replace('\n','').replace('\r','') # For some reason this cleans the data better than 'rstrip'
            output.write(text + '\n')
            output.close()
            self.count += 1
            self.analyzer.analyzeTweet(text)
        if time.time() - self.t0 > 60:
            print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            print ("Tweets Mined: %d" % self.count)
            self.analyzer.printResults()
            emoticon = clf.predict(self.analyzer.results())
            print (emoticons[emoticon])
            out = open("history", 'a')
            out.write(emoticons[emoticon]+"\n")
            out.close()
            print "------------------------------------------------------------"
            self.api.update_status("Twitter is feeling " + emoticons[emoticon] + " at " + datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S') + ' on ' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d') + "...Happy Holidays Class! Any questions?")
            print ("Twitter is feeling " + emoticons[emoticon] + " at " + datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S'))
            print "------------------------------------------------------------"
            return False # Stop the stream after 10 minutes
        return True
    
    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream


###############################################################################

if __name__ == '__main__':
    # Initialize the pre-determined text analyzer
    dal = readDictionary.readDAL()
    labmt = readDictionary.readLABMT()
    afinn = readDictionary.readAFINN()
         
    english = readDictionary.readEnglish()
     
    emoticons = readDictionary.readEmoticons()
     
    analyzer = Analysis.Analysis(dal, labmt, afinn, english)
    
    # Initialize the pre-determined classifier
    clf = Classifier.buildClassifier()
    
    infinite = True
    while(infinite):
        analyzer.reset()
        csl = CustomStreamListener(clf, analyzer, emoticons, api)
        stream = tweepy.streaming.Stream(auth, csl)
        stream.sample()