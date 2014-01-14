'''
Created on Dec 14, 2013

@author: Benjamin
'''

class DALAnalysis():
    
    import scipy.stats
    import readDictionary
    import TwitterTokenizer
    from collections import defaultdict as ddict
    import numpy as np
    
    dal = readDictionary.readDAL()
    
    #Pleasantness = ee mean is 1.85, sd is .36
    #Activation = aa mean is  1.67, sd is .36
    #Imagery = ii mean is 1.54, sd is .63
    
    ee = scipy.stats.norm(1.85,.36)
    aa = scipy.stats.norm(1.67,.36)
    ii = scipy.stats.norm(1.54,.63)
    
    e = 0.0
    a = 0.0
    i = 0.0
    
    count = 0.0
    hit = 0.0
    dict = {}
    
    keys = ["Pleasant", "Cheerful", "Active", "Nasty", "Unpleasant", "Sad", "Passive", "Nice", "HighlyImaged", "PoorlyImaged"]
    
    for x in keys:
        dict[x] = ddict(float)
    
    english = readDictionary.readEnglish()
    
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
    
    def isHit(self, word):
        self.count += 1
        if not self.dal[word] == []:
            self.hit += 1
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
            hit = self.isHit(i)
            if hit:
                if self.isPleasant(i):
                    self.dict["pleasant"][i] += 1
                if self.isCheerful(i):
                    self.dict["cheerful"][i] += 1
                if self.isActive(i):
                    self.dict["active"][i] += 1
                if self.isNasty(i):
                    self.dict["nasty"][i] += 1
                if self.isUnpleasant(i):
                    self.dict["unpleasant"][i] += 1
                if self.isSad(i):
                    self.dict["sad"][i] += 1
                if self.isPassive(i):
                    self.dict["passive"][i] += 1
                if self.isNice(i):
                    self.dict["nice"][i] += 1
                if self.isHighlyImaged(i):
                    self.dict["highlyImaged"][i] += 1
                if self.isPoorlyImaged(i):
                    self.dict["poorlyImaged"][i] += 1
                    
        for i in self.keys:
            array = self.np.array(self.dict[i].values())
            print i + " : " + str(self.np.sum(array)/self.hit*100) + "%"
    
    def analyzeTweet(self, tweet):
        for i in self.tokenizeTweet(tweet):
            hit = self.isHit(i)
            if hit:
                if self.isPleasant(i):
                    self.dict["pleasant"][i] += 1
                if self.isCheerful(i):
                    self.dict["cheerful"][i] += 1
                if self.isActive(i):
                    self.dict["active"][i] += 1
                if self.isNasty(i):
                    self.dict["nasty"][i] += 1
                if self.isUnpleasant(i):
                    self.dict["unpleasant"][i] += 1
                if self.isSad(i):
                    self.dict["sad"][i] += 1
                if self.isPassive(i):
                    self.dict["passive"][i] += 1
                if self.isNice(i):
                    self.dict["nice"][i] += 1
                if self.isHighlyImaged(i):
                    self.dict["highlyImaged"][i] += 1
                if self.isPoorlyImaged(i):
                    self.dict["poorlyImaged"][i] += 1
    
    def analyzeTweet2(self, tweet):
        for i in self.tokenizeTweet(tweet):
            hit = self.isHit(i)
            if hit:
                self.e += self.dal[i][0]
                self.a += self.dal[i][1]
                self.i += self.dal[i][2]
                for j in self.keys:
                    if getattr(self, "is" + j)(i):
                        self.dict[j][i] += 1
    
    def results(self):
        print "hit rate: " + str(self.hit/self.count*100) + "%"
        print "mean pleasantness(e): " + str(self.e/self.count)
        print "mean activation(a): " + str(self.a/self.count)
        print "mean imagery(i): " + str(self.i/self.count)
        
        for i in self.keys:
            array = self.np.array(self.dict[i].values())
            print i + ": " + str(self.np.sum(array)/self.hit*100) + "%"

###############################################################################

if __name__ == '__main__':
    dal = DALAnalysis()
    dal.analyze('results')