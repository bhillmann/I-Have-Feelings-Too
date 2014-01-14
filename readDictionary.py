'''
Created on Dec 6, 2013

@author: Benjamin
'''

import collections
import os

def readDAL():
    input = open("Dictionary of Affected Language/bareDictionary.txt", 'r')
    dictionary = collections.defaultdict(list)
    for line in input:
        line = line.rstrip()
        tokens = line.split(' ')
        scores = tokens[-3:]
        for i in range(len(scores)):
            scores[i] = float(scores[i])
        dictionary[tokens[0]] = scores
    input.close()
    return dictionary

def readLABMT():
    input = open("labMT 1.0/Data_Set_S1.txt", 'r')
    dictionary = collections.defaultdict(float)
    for line in input:
        line = line.rstrip()
        tokens = line.split('\t')
        dictionary[tokens[0]] = float(tokens[2])
    input.close()
    return dictionary

def readAFINN():
    input = open("AFINN/AFINN-111.txt", 'r')
    dictionary = collections.defaultdict(float)
    for line in input:
        line = line.rstrip()
        tokens = line.split('\t')
        dictionary[tokens[0]] = float(tokens[1])
    input.close()
    return dictionary

def readEnglish():
    english = set()
    for files in os.walk('SCOWL'):
        for path in files[2]:
            input = open('SCOWL/' + path, 'r')
            for line in input:
                english.add(line.rstrip().lower())
            input.close()
    return english

def readEmoticons():
    input = open("Emoticons/emoticons", 'r')
    array = []
    for line in input:
        line = line.split('\t')
        array.append(line[0])
    input.close()
    return array