'''
Created on Feb 17, 2014
data structure for expansion terms
@author: cx
'''
import json,math
class ExpTermC:
    
    def Init(self):
        self.term = ""
        self.query = ""
        self.qid = ""
        self.score = 0
        self.hFeature = {} #name->score
        
        
    def __init__(self,line = ""):
        self.Init()
        if "" != line:
            self.load(line)
        return
    
    
    def load(self,line):
#         print "loading exp term line [%s]" %(line)
        vCol = line.strip().split('\t')
#         print json.dumps(vCol)
        self.qid = vCol[0]
        self.query = vCol[1]
        self.term = vCol[2]
        if len(vCol) > 3:
            self.score = math.exp(float(vCol[3]))            
        if len(vCol) > 4:
            self.SetFeature(vCol[4])
        return True
    
    
    
    def SetFeature(self,FeatureStr):
        vF = FeatureStr.split(',')
        for feature in vF:
            lMid = feature.split('&')
            dim = lMid[0]
            value = float(lMid[1])
            self.hFeature[dim] = value
        return True
    
    def JoinFeatureStr(self):
        FeatureStr = ""
        for item in self.hFeature:
            FeatureStr += item + '&%f,' %(self.hFeature[item])
        return FeatureStr.strip(',')
    
    def dump(self):
        line = self.qid + "\t" + self.query + '\t' + self.term + '\t%f'%(math.log(self.score)) + '\t' + self.JoinFeatureStr() 
        return line
    
    
    def AddFeature(self,hFDict):
        for item in hFDict:
            if not item in self.hFeature:
                self.hFeature[item] = 0
            self.hFeature[item] += hFDict[item]
        return True
    
    def __deepcopy__(self,memo):
        Term = ExpTermC(self.dump())
        return Term
    def Key(self):
        return self.qid + "_"  +self.query + "_" + self.term
    
    
    
    def ExtractPRALengthFeature(self):
        hPRALen = {}
        for feature in self.hFeature:
            if not self.IsPRAFeature(feature):
                continue
            value = self.hFeature[feature]
            vCol = feature.split('#')
            PRALen = len(vCol) - 2
            PRALenName = 'CntPRALen%d' %(PRALen)
            if not PRALenName in hPRALen:
                hPRALen[PRALenName] = 0
            hPRALen[PRALenName] += value
        for item in hPRALen:
            self.hFeature[item] = hPRALen[item]
        return True
            
        
    def IsPRAFeature(self,feature):
        if '#' in feature:
            return True        



def ReadQExpTerms(InName):
    #read expansion terms from in name
    #group by qid
    llExpTerm = []
    
    p = 0
    llExpTerm.append([])
    for line in open(InName):
        line = line.strip()
        ExpTerm = ExpTermC(line)
        if llExpTerm[p] != []:
            if ExpTerm.qid != llExpTerm[p][0].qid:
                llExpTerm.append([])
                p += 1
        llExpTerm[p].append(ExpTerm)
    return llExpTerm 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

