'''
Created on Feb 10, 2014
linearly combine expansion term with query terms and re-ranking
input: query, lDoc, lTerm=[[term,weight]]
original query term weight is tf, weight is output of expansion alg
function: 1/Z(\sum_{t\in q) tf log p(t|d)) +  \sum_{t\in exp} w_t log p(t|d))
output: lDoc, re-ranked ,with new score

conf required:
    ctf: for inference
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr0/cx/cxPylib')
from cxBase.base import *
from IndriRelate.IndriInferencer import *
from IndriRelate.IndriPackedRes import *
from operator import attrgetter
import json
class QExpLinearCombinerC:
    
    def Init(self):
        self.IndriInferencer = LmInferencerC()
        self.CtfCenter = TermCtfC()
        
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.CtfCenter.Load(conf.GetConf("ctf"))
        return True
    
    def __init__(self,ConfIn = ""):
        self.Init()
        if "" != ConfIn:
            self.SetConf(ConfIn)
            
            
    
    def ReRank(self,query,lDoc,lTerm):
        #return a lReDoc, PackedIndriRes but with only DocNo and Score setted
        lLm = MakeLmForDocs(lDoc)
        
        lReDoc = []
        lAllTerm = lTerm        
        lQTerm = query.split()
        for term in lQTerm:
            lAllTerm.append([term,1.0/float(len(lQTerm))])        
#         print "rerank with [%s]" %(json.dumps(lAllTerm))
        for i in range(len(lDoc)):
            score = 0
            WeightSum = 0
            for WTerm in lAllTerm:
                InferScore = self.IndriInferencer.InferTerm(WTerm[0],lLm[i], self.CtfCenter)
#                 print 'term [%s]weight [%f] ' %(WTerm[0],WTerm[1])
#                 print ' lm score [%f]' %(InferScore)
                if InferScore != 0:
                    score += math.log(InferScore) * WTerm[1]
                WeightSum += WTerm[1]
            score = score / WeightSum
            Doc = PackedIndriResC()
            Doc.DocNo = lDoc[i].DocNo
            Doc.score = score
            lReDoc.append(Doc)
        lReDoc.sort(key=attrgetter('score'),reverse = True)
        return lReDoc
        
    
