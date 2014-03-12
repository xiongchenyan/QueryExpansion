'''
Created on Mar 7, 2014
use WOrig and 1-WOrig and weight associated with exp term to rerank docs
@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr0/cx/cxPylib')
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
from cxBase.base import *
from IndriRelate.IndriInferencer import *
from IndriRelate.IndriPackedRes import *
from operator import attrgetter
from base.ExpTerm import *
from CrossValidation.ParameterSet import *
import json
class WeightedReRankerC:
    
    def Init(self):
        self.IndriInferencer = LmInferencerC('twostage')
        self.CtfCenter = TermCtfC()
        self.WOrig = 0.5
        
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.CtfCenter.Load(conf.GetConf("ctfpath"))
        self.WOrig = float(conf.GetConf("worig"))
        return True
    
    def __init__(self,ConfIn = ""):
        self.Init()
        if "" != ConfIn:
            self.SetConf(ConfIn)
            
    def SetParameter(self,ParaSet):
        if "worig" in ParaSet.hPara:
            self.WOrig = float(ParaSet.hPara['worig'])
        return True
                
    
    def ReRank(self,lDoc,lExpTerm):
        #return a lReDoc, PackedIndriRes but with only DocNo and Score setted
        print "start reranking for q [%s] doc num [%d], expterm num [%d]" %(lExpTerm[0].query,len(lDoc),len(lExpTerm))
        for ExpTerm in lExpTerm:
            print ExpTerm.term + "\t%f" %(ExpTerm.score)
        
        
        lLm = MakeLmForDocs(lDoc)
        
        lReDoc = []
        query= lExpTerm[0].query
        TotalExpWeight = 0
        for i in range(len(lExpTerm)):            
            TotalExpWeight += lExpTerm[i].score
        if 0 != TotalExpWeight:
            for i in range(len(lExpTerm)):
                #normalization
                lExpTerm[i].score /= TotalExpWeight            

        for i in range(len(lDoc)):
            OrigQScore = self.IndriInferencer.InferQuery(query, lLm[i], self.CtfCenter)
#             OrigQScore = lDoc[i].score            
            ExpScore = 0
            for WTerm in lExpTerm:
                InferScore = self.IndriInferencer.InferTerm(WTerm.term,lLm[i], self.CtfCenter)
#                 print 'term [%s]weight [%f] ' %(WTerm[0],WTerm[1])
#                 print ' lm score [%f]' %(InferScore)
                if InferScore != 0:
                    ExpScore += math.log(InferScore) * WTerm.score            
            TotalScore = self.WOrig * OrigQScore + (1-self.WOrig) * ExpScore            
            Doc = PackedIndriResC()
            Doc.DocNo = lDoc[i].DocNo
            Doc.score = TotalScore
            lReDoc.append(Doc)
        lReDoc.sort(key=attrgetter('score'),reverse = True)
        
        print "rerank res:\n%s" %(json.dumps(SegDocNoFromDocs(lReDoc),indent=1))
        
        return lReDoc
        
    


def WeightedReRankerUnitTest(ConfIn):
    #unit test re ranker
    
    WeightedReRanker = WeightedReRankerC(ConfIn)
    conf = cxConf(ConfIn)
    QueryExpTermIn = conf.GetConf('in')
    CashDir = conf.GetConf('cashdir')
    OutName = conf.GetConf('out')
    NumOfReRankDoc = conf.GetConf('numofrerankdoc')
    
    llExpTerm = ReadQExpTerms(QueryExpTermIn)
    out = open(OutName,'w')
    
    for lExpTerm in llExpTerm:
        query = lExpTerm[0].query
        qid = lExpTerm[0].qid
        lDoc = ReadPackedIndriRes(CashDir + "/" + query,NumOfReRankDoc)
        lReDoc = WeightedReRanker.ReRank(lDoc, lExpTerm)
        lOut = OutReRankRes(qid,lReDoc)
        print >> out,'\n'.join(lOut[0:min(50,len(lOut))])
        
    out.close()
    return True


def OutReRankRes(qid,lReDoc):
    #output a indri out format
    lOut = []
    for i in range(len(lReDoc)):
        lOut.append("%s Q0 %s %d %f Expansion" %(qid,lReDoc[i].DocNo,i + 1,lReDoc[i].score))
    return lOut    
    
    
    
