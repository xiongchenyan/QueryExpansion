'''
Created on Jun 1, 2014
expansion from freebase rank
input: a rank of freebase object for each query, with score
do: treat these objects as documents, and run tf*log(ctf)*(normalized doc score) as expansion
output: a list of expansion term. 
@author: cx
'''

'''
implemented june 1 2014
tbd: update method in ExpansionSingleRunCenter
    test
    run and evaluate prf from facc and google search api
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from cxBase.base import cxBaseC,cxConf
from base.ExpTerm import *
from FbObjCenter.FbObjCacheCenter import *
from CrossValidation.ParameterSet import *
from IndriRelate.CtfLoader import *
from IndriRelate.IndriInferencer import LmBaseC
from cxBase.TextBase import TextBaseC     
import math
class FreebaseObjRankExpansionC(cxBaseC):
    #api required to be called in expansion pipeline:
        #init and load data in SetConf()
        #set parameter to modify parameter 
        #process to process
    def Init(self):
        #data
        self.CtfCenter = TermCtfC()
        self.hQueryObjRank = {} #qid->[[obj id,ranking score]] rank
        self.ObjCenter = FbObjCacheCenterC() #its parameter must be manually set, not via conf
        self.QObjRankInName = ""
        #paths and paras
        self.NumOfExpTerm = 10
        self.NumOfObjUsed = 10
        
        return
    
    
    @staticmethod
    def ShowConf():
        print "ctfpath\nqueryobjrank\nobjcachedir\nnumofexpterm\nnumofobj"
    
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.NumOfObjUsed = int(conf.GetConf('numofobj',self.NumOfObjUsed))
        self.CtfCenter.Load(conf.GetConf('ctfpath'))        
        self.ObjCenter.SetConf(ConfIn)
        self.NumOfExpTerm = int(conf.GetConf('numofexpterm',self.NumOfExpTerm))
        self.QObjRankInName = conf.GetConf('queryobjrank')
        return
    
    
    def LoadQObjRank(self,InName):
        if len(self.hQueryObjRank) != 0:
                return 
        for line in open(InName):
            vCol = line.strip().split('\t')
            qid = vCol[0]
            ObjId = vCol[2]
            score = float(vCol[4])
            if not qid in self.hQueryObjRank:
                self.hQueryObjRank[qid] = [[ObjId,score]]
            else:
                if len(self.hQueryObjRank[qid]) < self.NumOfObjUsed:
                    self.hQueryObjRank[qid].append([ObjId,score])
                    
                    
            
        #normalize score to probability
        for item in self.hQueryObjRank:
            total = 0
            for objid,score in self.hQueryObjRank[item]:
                total += score
            if total != 0:
                for i in range(len(self.hQueryObjRank[item])):
                    self.hQueryObjRank[item][i][1] /= total
        
                
            
            
    def FilterByLength(self,term):
        return len(term) < 3        
            
    def DiscardQueryTerm(self,query,term):
        if term.lower() in query.lower():
            return True
        return False
    
    def Process(self,qid,query,lDoc=[]):
        #get obj rank
        #for each obj, get its term from description, and add to its score        

        self.LoadQObjRank(self.QObjRankInName)        
        lExpTerm = []
        hTerm = {} #index to lExpTerm
        
        if not qid in self.hQueryObjRank:
            print "obj rank for q [%s] not read" %(qid)
            return lExpTerm
        print "working on q [%s][%s]" %(qid,query)
        for ObjId,DocScore in self.hQueryObjRank[qid]:
            print "q [%s] related obj [%s] score [%f]" %(qid,ObjId,DocScore)
            desp = self.ObjCenter.FetchObjDesp(ObjId)
            Lm = LmBaseC()            
            Lm.AddRawText(TextBaseC.RawClean(desp))
            for term in Lm.hTermTF:
                if self.FilterByLength(term):
                    continue
                
                if self.DiscardQueryTerm(query,term):
                    continue
                
                tf = Lm.GetTFProb(term)
                idf = self.CtfCenter.GetLogIdf(term)
                score = tf * idf * DocScore #doc score is a normalized probability
#                 print "term [%s] score [%f]" %(term,score)
                if not term in hTerm:
                    ExpTerm = ExpTermC()
                    ExpTerm.term = term
                    ExpTerm.score = score
                    ExpTerm.qid = qid
                    ExpTerm.query = query
                    lExpTerm.append(ExpTerm)
                    hTerm[term] = len(lExpTerm) - 1
                else:
                    lExpTerm[hTerm[term]].score += score
#                 print "term [%s] total score [%s]" %(term,lExpTerm[hTerm[term]].score)
        lExpTerm.sort(key=lambda item: item.score,reverse = True)
        return lExpTerm[:self.NumOfExpTerm]
    
    
    def ExpandUsingOneObj(self,qid,query,ObjId,lDoc = []):
       
        lExpTerm = []
        hTerm = {} #index to lExpTerm       

        print "working on q [%s][%s]" %(qid,query)
        DocScore = 1.0
        desp = self.ObjCenter.FetchObjDesp(ObjId)
        Lm = LmBaseC()            
        Lm.AddRawText(TextBaseC.RawClean(desp))
        for term in Lm.hTermTF:
            if self.FilterByLength(term):
                continue
            
            if self.DiscardQueryTerm(query,term):
                continue
            
            tf = Lm.GetTFProb(term)
            idf = self.CtfCenter.GetLogIdf(term)
            score = tf * idf * DocScore #doc score is a normalized probability
#                 print "term [%s] score [%f]" %(term,score)
            if not term in hTerm:
                ExpTerm = ExpTermC()
                ExpTerm.term = term
                ExpTerm.score = score
                ExpTerm.qid = qid
                ExpTerm.query = query
                lExpTerm.append(ExpTerm)
                hTerm[term] = len(lExpTerm) - 1
            else:
                lExpTerm[hTerm[term]].score += score
#                 print "term [%s] total score [%s]" %(term,lExpTerm[hTerm[term]].score)
        lExpTerm.sort(key=lambda item: item.score,reverse = True)
        return lExpTerm[:self.NumOfExpTerm]
    
    
    def SetParameter(self,ParaSet):
        
        if 'numofexpterm' in ParaSet.hPara:
            self.NumOfExpTerm = int(ParaSet.hPara['numofexpterm'])
            print "set para numofexpterm [%d]" %(self.NumOfExpTerm)
        if 'numofobj' in ParaSet.hPara:
            self.NumOfObjUsed = int(ParaSet.hPara['numofobj'])
            print "set para numofobj [%d]" %(self.NumOfObjUsed)
        
        return True