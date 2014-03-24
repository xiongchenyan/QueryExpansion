'''
Created on Mar 12, 2014
cross validation for unsupervised expansion methods 
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr0/cx/cxPylib')
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

import copy
from UnsupervisePipeline.ExpansionSingleRunPipe import *
from CrossValidation.ParameterSet import *
from CrossValidation.RandomSplit import *


class UnsupervisedExpansionCVC(object):
    
    def Init(self):
        self.EvaOutDir = ""
        self.QueryInName = ""
        self.lPara = [] #to explore para sets
        self.FoldNum = 5
        self.SingleRunPipe = ExpansionSingleRunPipeC()
        
        
    def __init__(self,ConfIn = ""):
        self.Init()
        if "" != ConfIn:
            self.SetConf(ConfIn)
        return
    
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.EvaOutDir = conf.GetConf("evaoutdir")
        self.QueryInName = conf.GetConf('in')
        self.FoldNum = int(conf.GetConf('k'))
        self.lPara = ReadParaSet(conf.GetConf('paraset'))
        if not os.path.exists(self.EvaOutDir):
            os.makedirs(self.EvaOutDir)
        self.SingleRunPipe.SetConf(ConfIn)
        return True
    
    
    @staticmethod
    def ShowConf():
        ExpansionSingleRunPipeC.ShowConf()
        print "evaoutdir\nin\nk\nparaset"
    
    
    
    def ProcessOneFold(self,lTrainQid,lTrainQuery,lTestQid,lTestQuery,FoldInd):
        #process one fold
        #pick best para in lTrains
        #get eva res in lTest
        #out: per q eva res of lTest
        
        
        print "start train:\n%s\ntest:\n%s" %(json.dumps(lTrainQuery),json.dumps(lTestQuery))
        
        #train
        self.SingleRunPipe.lParaSet = self.lPara
        self.SingleRunPipe.EvaOutDir = self.EvaOutDir + "/train_%d" %(FoldInd)
        
        self.SingleRunPipe.ProcessWithLoadQ(lTrainQid, lTrainQuery)
        BestMapP,BestNdcgP,BestErrP = self.SingleRunPipe.PickBestParaSet()
        print "best map p: %d\nbest ndcg p:%d\nbest err p:%d"%(BestMapP,BestNdcgP,BestErrP)
        #choose ndcg for now
        TestPara =  copy.deepcopy(self.SingleRunPipe.lParaSet[BestNdcgP])
        
        #test
        self.SingleRunPipe.lParaSet = [TestPara]
        self.SingleRunPipe.EvaOutDir = self.EvaOutDir + '/test_%d' %(FoldInd)
        llTestMeasure = self.SingleRunPipe.ProcessWithLoadQ(lTestQid, lTestQuery)
        
        
        lTestFoldRes = []
        for mea in llTestMeasure:
            lTestFoldRes.append(mea[0]) #only one dim for TestPara
                
        return lTestFoldRes,TestPara
    
    
    def ReadAndPartitionQuery(self):
        llTrainQid = []
        llTrainQuery = []
        llTestQuery = []
        llTestQid = []
        
        
        lData = []
        for line in open(self.QueryInName):
            lData.append(line.strip())
        llSplit = RandomSplit(lData,self.FoldNum)
        
        
        for lSplit in llSplit:
            lTrain= lSplit[0]
            lTest = lSplit[1]
            lTrainQid = []
            lTrainQuery = []
            lTestQid = []
            lTestQuery = []
            
            for Train in lTrain:
                qid,query = Train.split('\t')
                lTrainQid.append(qid)
                lTrainQuery.append(query)
            for Test in lTest:
                qid,query = Test.split('\t')
                lTestQid.append(qid)
                lTestQuery.append(query)
            llTrainQid.append(lTrainQid)
            llTrainQuery.append(lTrainQuery)
            llTestQid.append(lTestQid)
            llTestQuery.append(lTestQuery)
        return llTrainQid,llTrainQuery,llTestQid,llTestQuery
    
    
    
    def Process(self):
        EvaOut = open(self.EvaOutDir + "/CVEval",'w')
        AppliedParaOut = open(self.EvaOutDir + "/CVPara",'w')
        
        llTrainQid,llTrainQuery,llTestQid,llTestQuery = self.ReadAndPartitionQuery()
        MeanEva = AdhocMeasureC()
        cnt = 0
        for i in range(self.FoldNum):
            lTrainQid, lTrainQuery, lTestQid, lTestQuery = llTrainQid[i],llTrainQuery[i],llTestQid[i],llTestQuery[i] 
            lTestFoldRes,TestPara = self.ProcessOneFold(lTrainQid, lTrainQuery, lTestQid, lTestQuery, i)
            
            for QInd in range(len(lTestQid)):
                print >> EvaOut,lTestQid[QInd] + "\t" + lTestFoldRes[QInd].dumps(False)
                print >> AppliedParaOut, lTestQid[QInd] + "\t" + TestPara.dumps()
                MeanEva = MeanEva + lTestFoldRes[QInd]
                cnt += 1
                
        MeanEva = MeanEva / cnt 
        print >> EvaOut,"mean\t%s" %(MeanEva.dumps())
        
        EvaOut.close()
        AppliedParaOut.close()        
        return True
                
            
            
             

    
    
    
        
        

