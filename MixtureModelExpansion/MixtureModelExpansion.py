'''
Created on Mar 23, 2014

@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr0/cx/cxPylib')
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
from base.ExpansionBase import *
from operator import attrgetter
from CrossValidation.ParameterSet import *
from IndriRelate.IndriInferencer import *
import math

class MixtureModelExpansionC(QueryExpansionC):
    def Init(self):
        self.Lambda = 0.5
        self.MaxEmIte = 100
        self.EMTerminate = 0.01
        
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.Lambda = conf.GetConf('lambda')
        mid = conf.GetConf('maxemite')
        if "" != mid:
            self.MaxEmIte = int(mid)
        mid = conf.GetConf('emterminate')
        if '' != mid:
            self.EMTerminate = float(mid)
        return True
    
    
    def __init__(self,ConfIn = ""):
        super(MixtureModelExpansionC,self).__init__(ConfIn)
        self.Init()
        if "" != ConfIn:
            self.SetConf(ConfIn)
            
        return
    
    
    @staticmethod
    def ShowConf():
        super(MixtureModelExpansionC).ShowConf()
        print "lambda\nmaxemite 100\nemterminate 0.01"
        return True
    
    def SetParameter(self,ParaSet):
        super(MixtureModelExpansionC,self).SetParameter(ParaSet)
        if "lambda" in ParaSet.hPara:
            self.Lambda = float(ParaSet.hPara['lambda'])
        return True
    
    
    def Process(self,qid,query,lDoc):
        
        #form lLm
        #form lExpTerm (all terms in lDoc)        
        #init EM value (TF sum/Z)
        #E step
        #M step
        lLm = MakeLmForDocs(lDoc)
        lExpTerm = self.FormRawExpTermFromLm(qid, query, lLm)     
        lExpTerm = self.EM(lLm,lExpTerm)                                            
        return lExpTerm
        
    
    def EM(self,lLm,lExpTerm):
        lThisTw = [0] * len(lExpTerm) #hidden variable in EM
        lLastTw = list(lThisTw)
        IteNum = 0
        while IteNum < self.MaxEmIte:
            lThisTw = self.E(lExpTerm)
            if self.EMEnd(lLastTw,lThisTw):
                break
            lExpTerm = self.M(lThisTw,lLm,lExpTerm)            
            IteNum += 1           
        return lExpTerm
    
    
    def E(self,lExpTerm):
        lTw = [0] * len(lExpTerm)
        for i in range(len(lExpTerm)):
            term = lExpTerm[i].term
            CorpP = self.CtfCenter.GetCtfProb(term)
            lTw[i] = (1 - self.Lambda)*lExpTerm[i].score / ((1 - self.Lambda)*lExpTerm[i].score + self.Lambda * CorpP)
        return lTw
    
    def M(self,lTw,lLm,lExpTerm):
        Z = 0
        for i in range(len(lExpTerm)):
            for Lm in lLm:
                lExpTerm[i].score = Lm.GetTF(lExpTerm[i].term) * lTw[i]
                Z += lExpTerm[i].score
        if 0 != Z:
            for i in range(len(lExpTerm)):
                lExpTerm[i].score /= Z
        return lExpTerm
            
        
        
        
    def EMEnd(self,lLastTw,lThisTw):
        diff = 0
        for i in range(len(lLastTw)):
            diff += abs(lLastTw[i] - lThisTw[i])
        return diff/sum(lLastTw) < self.EMTerminate
            
    
    
    def FormRawExpTermFromLm(self,qid,query,lLm):
        #score is tf/Z
        lExpTerm = []
        hExpTerm = {} #term:index in lExpTerm
        Z = 0
        for Lm in lLm:
            for term in Lm.hTermTF:
                TF = Lm.GetTF(term)
                if not term in hExpTerm:
                    hExpTerm[term] = len(lExpTerm)
                    ExpTerm = ExpTermC()
                    ExpTerm.qid = qid
                    ExpTerm.query = query
                    ExpTerm.term = term
                    ExpTerm.score = 0
                    lExpTerm.append(ExpTerm)
                p = hExpTerm[term]
                lExpTerm[p].score += TF
                Z += TF
                
        for i in range(len(lExpTerm)):
            lExpTerm[i].score /= float(Z)
        return lExpTerm
                
                
    
def MixtureModelExpansionUnitTest(ConfIn):
    MixtureModelExpansion = MixtureModelExpansionC(ConfIn)
    conf = cxConf(ConfIn)
    QIn = conf.GetConf("in")
    ExpTermOut = conf.GetConf("out")
    CashDir = conf.GetConf("cashdir")
    NumOfIndriRes = int(conf.GetConf("prfdocnum"))
    
    out = open(ExpTermOut,'w')
    for line in open(QIn):
        line = line.strip()
        qid,query = line.split('\t')
        lDoc = ReadPackedIndriRes(CashDir + "/" + query,NumOfIndriRes)
        lExpTerm = MixtureModelExpansion.Process(qid, query, lDoc)
        for ExpTerm in lExpTerm:
            print >>out, ExpTerm.dump()
            
    out.close()
    return True
            
        
        
    
        