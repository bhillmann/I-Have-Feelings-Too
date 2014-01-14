'''
Created on Dec 14, 2013

@author: Benjamin
'''

import Analysis
import readDictionary
import TwitterTokenizer
import os
from sklearn import tree
from sklearn import cross_validation
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
import time


import numpy as np
from sklearn.svm import SVC

def datapoints(analyzer, emoticons):
    for files in os.walk('tweets/emoticontweets'):
        for path in files[2]:
            input = open('tweets/emoticontweets/' + path, 'r')
            for line in input:
                tok = TwitterTokenizer.Tokenizer(preserve_case=False)   
                tokenized = tok.tokenize(line)
                for a in range(len(emoticons)):
                    if emoticons[a] in tokenized:
                        analyzer.analyzeTweet(line)
                        x = analyzer.results()
                        yield x, a
                        analyzer.reset()
            input.close()

def writeDatapoints():
    dal = readDictionary.readDAL()
    labmt = readDictionary.readLABMT()
    afinn = readDictionary.readAFINN()
     
    english = readDictionary.readEnglish()
 
    emoticons = readDictionary.readEmoticons()
 
    analyzer = Analysis.Analysis(dal, labmt, afinn, english)
    
    X = open("X", 'w')
    Y = open("Y", 'w')
    X.close()
    Y.close()
    
    for p in datapoints(analyzer, emoticons):
        X = open("X", 'a')
        X.write(str(p[0]) + "\n")
        X.close()
        Y = open("Y", 'a')
        Y.write(str(p[1]) + "\n")
        Y.close()

def readDatapoints():
    x = open("X", 'r')
    X = []
    
    for line in x:
        line = line.rstrip()
        line = line.replace('[','').replace(']','')
        line = line.split(',')
        for i in range(len(line)):
            line[i] = float(line[i])
        X.append(line) 
    x.close()     
    
    Y = []
    y = open("Y", 'r')
    for line in y:
        line = line.rstrip()
        line = int(line)
        Y.append(line)
    y.close()
    return X, Y
 
def trainClassifier(clf, X, y, cv):
    t0 = time.time()
    clf.fit(X, y)
    if cv == True:
        scores = cross_validation.cross_val_score(clf, X, y, cv=5)
        print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    print ("Time Taken to Train Classifier: %0.2f" % (time.time() - t0))
    print ("------------------------------------------------------------")
    return clf

def buildClassifier():
    data = readDatapoints()     
    X = np.array(data[0])
    y = np.array(data[1])
                 
#     clf = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=1, random_state=0, n_jobs=4)
    
    clf = BernoulliNB()
    
    return trainClassifier(clf,X,y,False)

    ###############################################################################
    
    if __name__ == '__main__':    
    data = readDatapoints()     

    X = np.array(data[0])
    y = np.array(data[1])
    
    clfs = [tree.DecisionTreeClassifier(),
        BernoulliNB(),
        RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=1, random_state=0, n_jobs=4),
        ExtraTreesClassifier(n_estimators=10, max_depth=None, min_samples_split=1, random_state=0, n_jobs=4)]

    clfsNames = ["Decision Tree", "BernoulliNB", "Random Forest", "Extra Trees"]
    
    for i in range(len(clfs)):
        print (clfsNames[i])
        trainClassifier(clfs[i],X,y,True)