'''
Created on Mar 7, 2014
indri expansion baseline
follow ExpansionBase
output a list of terms (can be used to re-rank, can also be used as a feature)



@author: cx
'''







'''
sep 5 2014
add expansion using external rank.
SetConf add externalrank
load external rank from conf (docno\tscore) (at set conf)

for each qid, fetch its externalrank (if has)
then re-order the lDoc by the setted score
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

class IndriExpansionC(QueryExpansionC):
    
    
    def Init(self):
        super(IndriExpansionC,self).Init()
        self.UseIdf = True
        self.IdfWeight = 0.5
        self.hTargetTerm = {} #record all target terms, if empty, then no filtering
        self.hExternalRank = {} #keep all external rank, if empty, then not using 
        
    def SetConf(self,ConfIn):
        super(IndriExpansionC,self).SetConf(ConfIn)
        conf = cxConf(ConfIn)
        TargetTermInName = conf.GetConf('targettermset')
        if "" != TargetTermInName:
            self.LoadTargetTerm(TargetTermInName)
            print "load target term set from [%s]" %(TargetTermInName)
        self.IdfWeight = conf.GetConf('idfweight',0.5)
        self.Useidf = bool(int(conf.GetConf('useidf',1.0)))
        
        ExternalRankName = conf.GetConf('externalrank')
        if "" != ExternalRankName:
            self.LoadExternalRank(ExternalRankName)
            print 'load external rank'
        
        
    @staticmethod
    def ShowConf():
        QueryExpansionC.ShowConf()
        print "targettermset\nexternalrank"
        
    def LoadTargetTerm(self,InName):
        for line in open(InName):
            ExpTerm = ExpTermC(line.strip())
            self.hTargetTerm[ExpTerm.Key()] = True
            
    def InTargetTermSet(self,qid,query,term):
        if {} == self.hTargetTerm:
            return True
        ExpTerm = ExpTermC()
        ExpTerm.qid = qid
        ExpTerm.query = query
        ExpTerm.term = term
        return ExpTerm.Key() in self.hTargetTerm
    
    
    def LoadExternalRank(self,InName):
        self.hExternalRank = {}
        for line in open(InName):
            qid,docno,score =line.strip().split('\t')
            if not qid in self.hExternalRank:
                self.hExternalRank[qid] = {}
            self.hExternalRank[qid][docno] = float(score)
        return True
        
    def UseExternalRank(self,qid,lDoc):
        if  {} == self.hExternalRank:
            return lDoc
        
        if not qid in self.hExternalRank:
            return lDoc
        
        hExtRank = self.hExternalRank[qid] #docno->score
        lNewDoc = []
        for doc in lDoc:
            if doc.DocNo in hExtRank:
                doc.score = hExtRank[doc.DocNo]
                lNewDoc.append(doc)
        lNewDoc.sort(key=lambda item: item.score, reverse = True)
        return lNewDoc
        
        
           
        
    def Process(self,qid,query,lDoc):
        #process query and lDoc
        #output a list of exp term
        
        lExpTerm = []
        hExpTerm = {} #map from term to position in lExpTerm
        
        '''
        reorder,filter and set score by external rank        
        '''
        lDoc = self.UseExternalRank(qid,lDoc)        
        lDoc = lDoc[:self.PrfDocNum]        
        lLm = MakeLmForDocs(lDoc)        
        
        print "num of prf doc [%d]" %(len(lDoc))
        
        for i in range(len(lLm)):
            lm = lLm[i]
            doc = lDoc[i]
            DocLen = lm.len
            print "using [%s]" %(doc.DocNo)
            
            for term in lm.hTermTF:
                if "[OOV]" == term:
                    continue
                if not self.InTargetTermSet(qid, query, term):
                    continue
                TF = lm.GetTF(term)
                CTF = self.CtfCenter.GetCtfProb(term)
                weight = math.log((TF + self.DirMu * CTF)/(DocLen + self.DirMu)) + doc.score
                if self.UseIdf:
                    if CTF == 0:
                        CTF = 0.5
                    weight += (1-self.IdfWeight) * weight + self.IdfWeight * math.log(1.0/CTF)                
                
                if not term in hExpTerm:
                    ExpTerm = ExpTermC()
                    ExpTerm.qid = qid
                    ExpTerm.query = query
                    ExpTerm.term = term
                    ExpTerm.score = 0
                    lExpTerm.append(ExpTerm)
                    hExpTerm[term] = len(lExpTerm) - 1
                lExpTerm[hExpTerm[term]].score += math.exp(weight)            
        lExpTerm.sort(key=attrgetter('score'), reverse=True)
        lExpTerm = lExpTerm[0:int(min(self.NumOfExpTerm,len(lExpTerm)))]
        
        lExpTerm = NormalizeExpTermWeight(lExpTerm)
#         self.NormalizeExpTermWeight(lExpTerm)
        #normalized exp score
        print "get [%d] exp term" %(len(lExpTerm))
        return lExpTerm
    
    
    
    def ExpandUsingOneObj(self,qid,query,DocNo,lDoc):
        lNewDoc = []
        DocScore = math.log(1.0)
        for doc in lDoc:
            if doc.DocNo == DocNo:
                doc.score = DocScore
                lNewDoc.append(doc)
                break
        print "expanding [%s][%s] using [%s] [%d] found" %(qid,query,DocNo,len(lNewDoc))
        return self.Process(qid, query, lNewDoc)
        
    
    
    def SetParameter(self,ParaSet):
        super(IndriExpansionC,self).SetParameter(ParaSet)
        if 'useidf' in ParaSet.hPara:
            self.UseIdf = bool(ParaSet.hPara['useidf'])
        if 'idfweight' in ParaSet.hPara:
            self.IdfWeight = float(ParaSet.hPara['idfweight'])

        
    
    
def IndriExpansionUnitTest(ConfIn):
    IndriExpansion = IndriExpansionC(ConfIn)
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
        lExpTerm = IndriExpansion.Process(qid, query, lDoc)
        for ExpTerm in lExpTerm:
            print >>out, ExpTerm.dump()
            
    out.close()
    return True
    
                    
                
