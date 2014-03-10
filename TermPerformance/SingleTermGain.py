'''
Created on Feb 10, 2014
method:
    \cite:{Selecting Good Expansion Terms for Pseudo-Relevance Feedback}
input: 
    termin: qid\tquery\tterm
    qrel:
    depth:
    indriresdir: (indri cashed res)
    ctf: term corpus frequency (should be made for all expansion terms)
    w (as in paper) default 0.01
output: 
    qid\tquery\tterm\toriginal map\twith term map
doing:
    load and set qrel
    for each q:
        load doc, evaluate map
        for each q's term:
            re-rank doc, evaluate map, output a line
            the re-rank is done by class in ExpansionReranking
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr0/cx/cxPylib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
from cxBase.base import cxConf
from IndriRelate.IndriInferencer import *
from IndriRelate.IndriPackedRes import *
from AdhocEva.AdhocEva import *
from ExpansionReranker.LinearCombiner import QExpLinearCombinerC


class SingleTermGainC:
    
    def Init(self):
        self.IndriResDir = ""
        self.LinearReranker = QExpLinearCombinerC()
        self.Evaluator = AdhocEvaC()
        self.NewTermW = 0.01
        self.UseMeasure = 'map'
        self.ReRankDocDepth = 50
    
    
    def __init__(self,ConfIn = ""):
        self.Init()
        if "" != ConfIn:
            self.SetConf(ConfIn)
        return
        
    def SetConf(self,ConfIn):
        self.LinearReranker.SetConf(ConfIn)
        self.Evaluator.SetConf(ConfIn)
        
        conf = cxConf(ConfIn)
        self.IndriResDir = conf.GetConf('indriresdir')
        self.NewTermW = float(conf.GetConf('newtermweight'))
        self.QTermInName = conf.GetConf('in')
        self.OutName = conf.GetConf('out')
        
        
    def EvaluaterPerTerm(self,qid,query,term,lDoc):
        print "q[%s] term [%s]" %(query, term)
        lTerm = []
        if term != "":
            lTerm = [[term,self.NewTermW]]
        lReDoc = self.LinearReranker.ReRank(query, lDoc, lTerm)
        
        lReDocId = []
        for ReDoc in lReDoc:
            lReDocId.append(ReDoc.DocNo)
        lEvaRes = self.Evaluator.EvaluatePerQ(qid, lReDocId)
        ResScore = 0
        for EvaRes in lEvaRes:
            if EvaRes[0] == self.UseMeasure:
                ResScore = EvaRes[1]
                break
        return ResScore
    
    
    def EvaluateFile(self):        
        CurrentQ = ""
        CurrentQid = ""
        lTerm = []
        out = open(self.OutName,'w')
        
        for line in open(self.QTermInName):
            line = line.strip()
            vCol = line.split('\t')
            qid = vCol[0]
            query = vCol[1]
            term = vCol[2]
            if CurrentQ == "":
                CurrentQ = query
                CurrentQid = qid
            if CurrentQ != query:
                print "working query [%s]" %(CurrentQ)
                InitScore,lTermScore = self.EvaluatePerQ(CurrentQid, CurrentQ, lTerm)
                for i in range(len(lTerm)):
                    print >>out, qid + '\t' + query + '\t' + lTerm[i] + '\t%f\t%f' %(InitScore,lTermScore[i])
                CurrentQ = query
                CurrentQid = qid
                lTerm = []
            lTerm.append(term)
        print "working query [%s]" %(CurrentQ)
        InitScore,lTermScore = self.EvaluatePerQ(CurrentQid, CurrentQ, lTerm)
        for i in range(len(lTerm)):
            print >>out, qid + '\t' + query + '\t' + lTerm[i] + '\t%f\t%f' %(InitScore,lTermScore[i])        
        out.close()        
        return True
    
    def EvaluatePerQ(self,qid,query,lTerm):
        lDoc = ReadPackedIndriRes(self.IndriResDir + "/" + query,self.ReRankDocDepth)
        InitScore = self.EvaluaterPerTerm(qid,query,"",lDoc)
        lTermScore = []
        for term in lTerm:
            lTermScore.append(self.EvaluaterPerTerm(qid, query, term, lDoc))
        return InitScore,lTermScore
        
        

            



