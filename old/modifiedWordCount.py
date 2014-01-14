import string
import re


def wordCount(filename):#function takes the name of a text file as the parameter, and returns a dictionary with key assigned to the words found in the text, and values assigned to the number of times that word appeared
    inFile = open(filename, 'rU')
    words = inFile.read()
    inFile.close()
    words = words.split()
    freq = {}
    for word in words:
        word = word.strip(string.punctuation)
        word = word.lower()
        pattern = '-*'
        strippedList = re.split(pattern, word)
        for strippedWord in strippedList:
            strippedWord = strippedWord.strip(string.punctuation)
            if strippedWord in freq:
                freq[strippedWord] += 1
            else:
                freq[strippedWord] = 1
    return freq

freq = wordCount('results')



