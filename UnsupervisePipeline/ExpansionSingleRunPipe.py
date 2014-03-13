'''
Created on Mar 11, 2014
single run:
input: a ParaSet (or a list)
output: evaluation value (mean and per q's)
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
from AdhocEva.AdhocEva import *
from AdhocEva.AdhocMeasure import *
from IndriExpansionBaseline.IndriExpansion import *
from ExpansionReranker.WeightedReRanker import *
import os,json

class ExpansionSingleRunPipeC:
    
    def Init(self):
        self.CashDir = ""
        self.QueryIn = ""
        self.EvaOutDir = ""
        self.CtfPath = ""
        self.ConfIn = ""
        self.lParaSet = []
        self.lEvaRes = []
        self.NumOfReRankDoc = 50
        return
    
    
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.ConfIn = ConfIn
        self.CashDir = conf.GetConf("cashdir")
        self.QueryIn = conf.GetConf('in')
        self.EvaOutDir = conf.GetConf('evaoutdir')
        self.CtfPath = conf.GetConf('ctfpath')
        self.NumOfReRankDoc = int(conf.GetConf('rerankdepth'))
        if not os.path.exists(self.EvaOutDir):
            os.makedirs(self.EvaOutDir)
        self.lParaSet = ReadParaSet(conf.GetConf('paraset'))
        print "load conf finished, going to test [%d] para sets" %(len(self.lParaSet))
        return True
    
    def __init__(self,ConfIn = ""):
        self.Init()
        if "" != ConfIn:
            self.SetConf(ConfIn)
        return
    
    
    
    
    def ProcessPerQ(self,qid,query):
        #load ldocs
        #for each para
            #call process for one para
            #record performance
        #return llEvaRes, the performance of this qid at all paras                
        lEvaRes = []        
        lDoc = ReadPackedIndriRes(self.CashDir + '/' + query,self.NumOfReRankDoc)        
        for ParaSet in self.lParaSet:
            lEvaRes.append(self.ProcessPerQWithOnePara(qid, query, lDoc, ParaSet))        
        return lEvaRes 
    
    
    def ProcessPerQWithOnePara(self,qid,query,lDoc,ParaSet):
        EvaMeasure = AdhocMeasureC()
        
        #set parameters
        IndriExpansion = IndriExpansionC(self.ConfIn)
        WeightedReRanker = WeightedReRankerC(self.ConfIn)
        AdhocEva = AdhocEvaC(self.ConfIn)
        
        IndriExpansion.SetParameter(ParaSet)
        WeightedReRanker.SetParameter(ParaSet)
        #AdhocEva not parameter to switch
        
        print "start run [%s][%s] with para [%s]" %(qid,query,json.dumps(ParaSet.__dict__))
        
        #expand
        lExpTerm = IndriExpansion.Process(qid, query, lDoc)
        print "exp done"
        #reranking
        lReRankedDoc = WeightedReRanker.ReRank(lDoc, lExpTerm)
        print "re ranking done"
        #evaluation
        EvaMeasure = AdhocEva.EvaluatePerQ(qid, AdhocEva.SegDocNoFromDocs(lReRankedDoc))
        print "eva done"
        return EvaMeasure
    
    
    
    def Process(self):
        #general processor, deal with things in self.QueryIn, output to self.EvaOutDir
        #output requirement:
            #mean eva res: parameter combination(paraname:value )\tevaluation measure (mean)
            #a per query evaluation results, file name(parameter combination), with standard evaluation output
        
        
        #read a qid\tquery
        #get lEvaRes (dim 1: para)
        #put to a llOveralEvaRes. (dim 2: para, dim 1: query)
        
        #output per q-para res
        #calc per para mean and output to one file        
        
        llOveralEvaRes = []
        lQid = []
        lQuery = []
        for line in open(self.QueryIn):
            line = line.strip()
            qid,query = line.split('\t')
            lQid.append(qid)
            lQuery.append(query)
            lEvaRes = self.ProcessPerQ(qid, query)
            llOveralEvaRes.append(lEvaRes)
            
        print "runs finished, wrap up evaluation results"
        self.OutPerQPerParaRes(lQid,lQuery,llOveralEvaRes)
        self.OutMeanPerPara(llOveralEvaRes) 
        
        
        print "finished"
        
        return True
    
    
    def ProcessWithLoadQ(self,lQid,lQuery):
        llOveralEvaRes = []
        self.lQid = lQid
        self.lQuery = lQuery
        for i in range(len(lQid)):
            qid = lQid[i]
            query = lQuery[i]
            lEvaRes = self.ProcessPerQ(qid, query)
            llOveralEvaRes.append(lEvaRes)
            
        print "runs finished, wrap up evaluation results"
        self.OutPerQPerParaRes(lQid,lQuery,llOveralEvaRes)
        self.OutMeanPerPara(llOveralEvaRes) 
        
        
        print "this set of query finished"        
        return llOveralEvaRes
        
    
    
    def PickBestParaSet(self):
        #must run after process
        if len(self.lEvaRes) == 0:
            print "pick best para need to run process first"
            return -1,-1,-1
        BestMapP = 0
        BestNdcgP = 0
        BestErrP = 0
        
        for i in range(len(self.lEvaRes)):
            if self.lEvaRes[i].map > self.lEvaRes[BestMapP].map:
                BestMapP = i
            if self.lEvaRes[i].ndcg > self.lEvaRes[BestNdcgP].ndcg:
                BestNdcgP = i
            if self.lEvaRes[i].err > self.lEvaRes[BestErrP].err:
                BestErrP = i                
        return BestMapP,BestNdcgP,BestErrP
        
    
    
    def OutPerQPerParaRes(self,lQid,lQuery,llOveralEvaRes):
        if not os.path.exists(self.EvaOutDir):
            os.makedirs(self.EvaOutDir)
#         print "outputing:\n%s" %(json.dumps(lQid,indent=1))
        for ParaP in range(len(self.lParaSet)):
            out = open(self.EvaOutDir + "/" + self.lParaSet[ParaP].dumps(),'w')
            para = self.lParaSet[ParaP]
            EvaMean = AdhocMeasureC()
            for QIndex in range(len(lQid)):
                EvaRes = llOveralEvaRes[QIndex][ParaP]
                query = lQuery[QIndex]
                qid = lQid[QIndex]
                
                print >> out,"%s\t%s" %(qid,EvaRes.dumps())
                EvaMean = EvaMean + EvaRes
            EvaMean = EvaMean / float(len(lQid))
            print >> out,"mean\t%s" %(EvaMean.dumps())
            out.close()              
        return True
    
    
    def OutMeanPerPara(self,llOveralEvaRes):   
        if not os.path.exists(self.EvaOutDir):
            os.makedirs(self.EvaOutDir)     
        out = open(self.EvaOutDir + "/MeanVsPara",'w')
        self.lEvaRes = []
        for ParaP in range(len(self.lParaSet)):
            EvaMean = AdhocMeasureC()
            para = self.lParaSet[ParaP]
            for i in range(len(llOveralEvaRes)):
                EvaMean = EvaMean + llOveralEvaRes[i][ParaP]
            EvaMean = EvaMean / len(llOveralEvaRes)
            print >> out,"%s\t%s" %(para.dumps(),EvaMean.dumps())    
            self.lEvaRes.append(EvaMean)   
        out.close()
        
        return True
        
        
        
    
