'''
Created on Mar 7, 2014
indri expansion baseline
follow ExpansionBase
output a list of terms (can be used to re-rank, can also be used as a feature)



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

class IndriExpansionC(QueryExpansionC):
    
    def Process(self,qid,query,lDoc):
        #process query and lDoc
        #output a list of exp term
        
        lExpTerm = []
        hExpTerm = {} #map from term to position in lExpTerm
        
        lLm = MakeLmFromDoc(lDoc)
        
        for i in range(len(lLm)):
            lm = lLm[i]
            doc = lDoc[i]
            DocLen = lm.len
            for term in lm.hTermTF:
                TF = lm.GetTF(term)
                CTF = self.CtfCenter.GetCtfProb(term)
                weight = math.log((TF + self.DirMu * CTF)/(DocLen + self.DirMu)) + doc.score
                if not term in hExpTerm:
                    ExpTerm = ExpTermC()
                    ExpTerm.qid = qid
                    ExpTerm.query = query
                    ExpTerm.term = term
                    ExpTerm.score = 0
                    lExpTerm.append(ExpTerm)
                    hExpTerm[term] = len(lExpTerm) - 1
                lExpTerm[hExpTerm[term]].score += math.exp(weight)
            lExpTerm[hExpTerm[term]].score = math.log(lExpTerm[hExpTerm[term]].score)
        lExpTerm.sort(key=attrgetter(score), reverse=True)
        lExpTerm = lExpTerm[0:min(self.NumOfExpTerm,len(lExpTerm))]
        return lExpTerm
    
    def SetParameter(self,ParaSet):
        if 'numofexpterm' in ParaSet.hPara:
            self.NumOfExpTerm = ParaSet.hPara['numofexpterm']
        if 'dirmu' in ParaSet.hPara:
            self.DirMu = ParaSet.hPara['dirmu']
        if 'prfdocnum' in ParaSet.hPara:
            self.PrfDocNum = ParaSet.hPara['prfdocnum']
        return True
        
    
    
def IndriExpansionUnitTest(ConfIn):
    IndriExpansion = IndriExpansionC(ConfIn)
    conf = cxConf(ConfIn)
    QIn = conf.LoadConf("in")
    ExpTermOut = conf.LoadConf("out")
    CashDir = conf.LoadConf("cashdir")
    NumOfIndriRes = int(conf.LoadConf("prfdocnum"))
    
    Out = open(ExpTermOut,'w')
    for line in open(QIn):
        line = line.strip()
        qid,query = line.split('\t')
        lDoc = ReadPackedIndriRes(CashDir + "/" + query,NumOfIndriRes)
        lExpTerm = IndriExpansion.Process(qid, query, lDoc)
        for ExpTerm in lExpTerm:
            print >>out, ExpTerm.dump()
            
    out.close()
    return True
    
                    
                
