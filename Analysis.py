'''
Created on Dec 14, 2013

@author: Benjamin
'''

import readDictionary

class Analysis:
    
    import scipy.stats
    import TwitterTokenizer
    from collections import defaultdict as ddict
    import numpy as np
    from itertools import repeat

    def __init__(self, dal, labmt, afinn, english):
        self.dal = dal
        self.labmt = labmt
        self.afinn = afinn
        self.english = english
        
        self.hh = self.scipy.stats.norm(5.38,1.08)        
        
        #Pleasantness = ee mean is 1.85, sd is .36
        #Activation = aa mean is  1.67, sd is .36
        #Imagery = ii mean is 1.54, sd is .63
            
        self.ee = self.scipy.stats.norm(1.85,.36)
        self.aa = self.scipy.stats.norm(1.67,.36)
        self.ii = self.scipy.stats.norm(1.54,.63)
    
        self.e = 0.0
        self.a = 0.0
        self.i = 0.0
    
        self.labmtSum = 0.0
        self.afinnSum = 0.0
    
        self.count = 0.0
        self.dalHit = 0.0
        self.labmtHit = 0.0
        self.afinnHit = 0.0
        self.dict = {}
    
        self.keys = ["Pleasant", "Cheerful", "Active", "Nasty", "Unpleasant", "Sad", "Passive", "Nice", "HighlyImaged", "PoorlyImaged"]
        self.positive = 0.0
        self.negative = 0.0
        self.happy = 0.0
        self.pain = 0.0
    
        for x in self.keys:
            self.dict[x] = self.ddict(float)
            
    def reset(self):   
        self.e = 0.0
        self.a = 0.0
        self.i = 0.0
    
        self.labmtSum = 0.0
        self.afinnSum = 0.0
    
        self.count = 0.0
        self.dalHit = 0.0
        self.labmtHit = 0.0
        self.afinnHit = 0.0
        self.dict = {}

        self.positive = 0.0
        self.negative = 0.0
        self.happy = 0.0
        self.pain = 0.0
    
        for x in self.keys:
            self.dict[x] = self.ddict(float)
    
    
    def isPleasant(self, word):
        e = self.dal[word][0]
        if self.ee.cdf(e) > .9:
            return True
        return False
    
    def isCheerful(self, word):
        e = self.dal[word][0]
        a = self.dal[word][1]
        if self.aa.cdf(a) > .75 and self.ee.cdf(e) > .75:
            return True
        return False
    
    def isActive(self, word):
        a = self.dal[word][1]
        if self.aa.cdf(a) > .9:
            return True
        return False
    
    def isNasty(self, word):
        e = self.dal[word][0]
        a = self.dal[word][1]
        if self.aa.cdf(a) > .75 and self.ee.cdf(e) < .25:
            return True
        return False
    
    def isUnpleasant(self, word):
        e = self.dal[word][0]
        if self.ee.cdf(e) < .1:
            return True
        return False
    
    def isSad(self, word):
        e = self.dal[word][0]
        a = self.dal[word][1]
        if self.ee.cdf(e) < .1 and self.aa.cdf(a) < .1:
            return True
        return False
    
    def isPassive(self, word):
        a = self.dal[word][1]
        if self.aa.cdf(a) < .1:
            return True
        return False
    
    def isNice(self, word):
        e = self.dal[word][0]
        a = self.dal[word][1]
        if self.ee.cdf(e) > .75 and self.aa.cdf(a) < .25:
            return True
        return False
    
    def isHighlyImaged(self, word):
        i = self.dal[word][2]
        if self.ii.cdf(i) > .9:
            return True
        return False
    
    def isPoorlyImaged(self, word):
        i = self.dal[word][2]
        if self.ii.cdf(i) < .1:
            return True
        return False
    
    def isHappy(self, word):
        h = self.labmt[word]
        if self.hh.cdf(h) > .9:
            return True
        return False
    
    def isPain(self, word):
        h = self.labmt[word]
        if self.hh.cdf(h) < .1:
            return True
        return False
    
    def isDALHit(self, word):
        if not self.dal[word] == []:
            self.dalHit += 1
            return True
        return False
    
    def isAFINNHit(self, word):
        if not self.afinn[word] == 0.0:
            self.afinnHit += 1
            return True
        return False
    
    def isLABMTHit(self, word):
        if not self.labmt[word] == 0.0:
            self.labmtHit += 1
            return True
        return False
    
    def read(self, dir):
        input = open(dir, 'r')
        tok = self.TwitterTokenizer.Tokenizer(preserve_case=False)
        for line in input:
            tokenized = tok.tokenize(line)
            for token in tokenized:
                if token in self.english:
                    yield token
        input.close()

    
    def tokenizeTweet(self, tweet):
        tok = self.TwitterTokenizer.Tokenizer(preserve_case=False)
        tokenized = tok.tokenize(tweet)
        for token in tokenized:
            if token in self.english:
                yield token
            
    
    def analyze(self, dir):
        for i in self.read(dir):
            self.count += 1
            dalHit = self.isDALHit(i)
            if dalHit:
                self.e += self.dal[i][0]
                self.a += self.dal[i][1]
                self.i += self.dal[i][2]
                for j in self.keys:
                    if getattr(self, "is" + j)(i):
                        self.dict[j][i] += 1                      
            afinnHit = self.isAFINNHit(i)
            if afinnHit:
                self.afinnSum += self.afinn[i]
                if self.afinn[i] > 0:
                    self.positive += 1
                else:
                    self.negative += 1
            labmtHit = self.isLABMTHit(i)
            if labmtHit:
                self.labmtSum += self.labmt[i]
                if self.isHappy(i):
                    self.happy += 1
                if self.isPain(i):
                    self.pain += 1
    
    def analyzeTweet(self, tweet):
        for i in self.tokenizeTweet(tweet):
            self.count += 1
            dalHit = self.isDALHit(i)
            if dalHit:
                self.e += self.dal[i][0]
                self.a += self.dal[i][1]
                self.i += self.dal[i][2]
                for j in self.keys:
                    if getattr(self, "is" + j)(i):
                        self.dict[j][i] += 1                      
            afinnHit = self.isAFINNHit(i)
            if afinnHit:
                self.afinnSum += self.afinn[i]
                if self.afinn[i] > 0:
                    self.positive += 1
                else:
                    self.negative += 1
            labmtHit = self.isLABMTHit(i)
            if labmtHit:
                self.labmtSum += self.labmt[i]
                if self.isHappy(i):
                    self.happy += 1
                if self.isPain(i):
                    self.pain += 1
    
    def results(self):
        r = []
        if self.dalHit > 0:
            r.append(self.e/self.dalHit)
            r.append(self.a/self.dalHit)
            r.append(self.i/self.dalHit)
            for x in self.keys:
                array = self.np.array(self.dict[x].values())
                r.append(self.np.sum(array)/self.dalHit)
        else:
            r = r + list(self.repeat(0.0,3))
            for x in self.keys:
                r.append(0.0)
        if self.afinnHit > 0:            
            r.append(self.afinnSum/self.afinnHit)
            r.append(self.positive/self.afinnHit)
        else:
            r = r + list(self.repeat(0.0,2))
        if self.labmtHit > 0:
            r.append(self.labmtSum/self.labmtHit)
            r.append(self.happy/self.labmtHit)
            r.append(self.pain/self.labmtHit)
        else:
            r = r + list(self.repeat(0.0,3))
        return r
            
    
    def printResults(self):
        print "DAL hit rate: " + str(self.dalHit/self.count*100) + "%"
        print "mean pleasantness(e): " + str(self.e/self.dalHit)
        print "mean activation(a): " + str(self.a/self.dalHit)
        print "mean imagery(i): " + str(self.i/self.dalHit)      
        for x in self.keys:
            array = self.np.array(self.dict[x].values())
            print x + ": " + str(self.np.sum(array)/self.dalHit*100) + "%"
        print "AFINN hit rate: " + str(self.afinnHit/self.count*100) + "%"
        print "mean AFINN: " + str(self.afinnSum/self.afinnHit)
        print "positive: " + str(self.positive/self.afinnHit*100) + "%"
        print "LABMT hit rate: " + str(self.labmtHit/self.count*100) + "%"
        print "mean LABMT: " + str(self.labmtSum/self.labmtHit)
        print "happy: " + str(self.happy/self.labmtHit*100) + "%"
        print "pain: " + str(self.pain/self.labmtHit*100) + "%"

###############################################################################

if __name__ == '__main__':
    dal = readDictionary.readDAL()
    labmt = readDictionary.readLABMT()
    afinn = readDictionary.readAFINN()
    
    english = readDictionary.readEnglish()   
    
    analyzer = Analysis(dal, labmt, afinn, english)
    analyzer.analyze('tweets/emoticontweets/dummy')
    analyzer.printResults()
    r = analyzer.results()
    for x in r:
        print x