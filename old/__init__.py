#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on Dec 5, 2013

@author: Benjamin
'''

import tweepy
import sys
import collections
import time

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
        
#     count = collections.defaultdict(int)
    
    t0 = time.time()
    
#     input = open('bareDictionary.txt', 'r')
    dal = collections.defaultdict(list)
    output = open('results', 'w')
    output.close()
    count = 0
    
#     for line in input:
#         line = line.rstrip()
#         tokens = line.split(' ')
#         dal[tokens[0]] = tokens[-3:]
#     input.close()
            
#     tokenizer = TwitterTokenizer.Tokenizer(preserve_case=False)
        
    def on_status(self, status):
        if status.lang == "en":
            output = open('results', 'a')
            text = status.text.replace('\n','').replace('\r','') # For some reason this cleans the data better than 'rstrip'
            output.write(text + '\n')
            output.close()
            self.count += 1
        if time.time() - self.t0 > 3600:
            print self.count
            return False # Stop the stream after 60 minutes seconds
        return True
            
#         if status.lang == "en":
#             tokenized = self.tokenizer.tokenize(status.text)
#             for token in tokenized:
#                 self.count[token] += 1
#         print self.count
#         return True # Don't kill the stream
    
    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream


###############################################################################

if __name__ == '__main__':
#     begin = time.time()
#     while(time.time() - begin < 60*60):
    x = 0
    while x==0:
        stream = tweepy.streaming.Stream(auth, CustomStreamListener())
        stream.sample()