'''
Created on Feb 13, 2014
expansion using random walk from Freebase
random walk results is done previously by BFSWalkerRun.py
input:
    a list of detail node file, one file for each BFS level.
        filename \t level
    for each such detail node file, each line:
        qid\tquery\tobject id\tlevel\tattributes(where terms come from)\tedges(where PRA feature come from)\ttypes
output is qid\tquery\tterm\tfeature&value\tfeature&value
    a q-t pair can appear multiple times, will be merged by following scripts
@author: cx
'''


'''
keep a obj->[PRA feature] dict
read RW result one level by one level
for each object, if it is for required query:
    get its PRAs
    add linked objects with PRA+edge to PRA dict
    output terms with PRA feature (the objects)
'''




import site
site.addsitedir('/bos/usr4/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr4/cx/cxPylib')
site.addsitedir('/bos/usr4/cx/PyCode/KnowledgeBase')
from cxBase.base import *
from FreebaseRandomWalk.FbRwNode import *
from FreebaseDumpRelate.FbDumpBasic import *
from operator import itemgetter
import copy
import json

class PRAFeatureCenterC:
    #I maintain obj->PRA feature, for saving memory way
    #PRAFeature = Edge ID#Edge ID
    def Init(self):
#         self.lEdge = []
        self.hEdge = {}
        self.hEdgeId = {}
        self.hObjPRA = {}
        return
    
    def __init__(self):
        self.Init()
        return
    
    def AddFeature(self,ObjId,Edge,lStStr = []):
        #no self-edge loop
#         if ObjId == StObj:
#             return True
#         lStStr = []        
#         if ("" != StObj) & (StObj in self.hObjPRA):
#             lStStr = self.hObjPRA[StObj]
        EdgeId = self.GetEdgeId(Edge)
        if not ObjId in self.hObjPRA:
            self.hObjPRA[ObjId] = []
#         print "add pra [%s][%s] with [%d] PRA\n%s" %(ObjId,Edge,len(lStStr),json.dumps(lStStr))
        if [] == lStStr:
            self.hObjPRA[ObjId].append(EdgeId)
        else:
            for StStr in lStStr:
#                 print "St-PRA:[%s]" %(StStr)
                self.hObjPRA[ObjId].append(StStr + '#' + EdgeId)             
        return True
    
    def __deepcopy__(self,memo):
        NewCenter = PRAFeatureCenterC()
        NewCenter.hEdge = copy.deepcopy(self.hEdge, memo)
        NewCenter.hEdgeId = copy.deepcopy(self.hEdgeId,memo)
        NewCenter.hObjPRA = copy.deepcopy(self.hObjPRA,memo)
        return NewCenter
    
    
    
    
    def GetEdgeId(self,Edge):
        if not Edge in self.hEdge:
            EdgeId = str(len(self.hEdge))
            self.hEdge[Edge] = EdgeId
            self.hEdgeId[EdgeId] = Edge            
        return self.hEdge[Edge]
    
    def GetPRAStr(self,ObjId):
#         lPRAStr = []
        if not ObjId in self.hObjPRA:
            return []
        lPRAId = self.hObjPRA[ObjId]
        lPRAStr = []
        for PRAId in lPRAId:
            lId = PRAId.split('#')
            PRAStr = ""
            for Id in lId:
                PRAStr += self.hEdgeId[Id] + '#'
            PRAStr = PRAStr.strip('#')
            lPRAStr.append(PRAStr)
        return lPRAStr
        




class QExpRandomWalkFbC:
    
    def Init(self):
#         self.hObjPRA = {} # the pra feature, obj->[pra1,pra2...]
        self.PRACenter = PRAFeatureCenterC()
        self.NewPRACenter = PRAFeatureCenterC()
        #all update of PRA is to NewPRACenter
            #and finish update after processed current level nodes. thus link between same level nodes are not contained
#         self.hReqQuery = {} #required query. read query. and put start node of query node as it self
        self.lRwFName = [] #the random walk res files. ordered by lvl
        self.hObjStNode = {} #record the start node for objects
        self.hNewObjStNode = {}
        self.OutName = ""
        
    def ReadQid(self,QidIn):
        for line in open(QidIn):
            vCol = line.strip().split('\t')
#             self.hReqQuery[vCol[1]] = vCol[0]
            self.hObjStNode[vCol[0] + "_" + vCol[1]] = [vCol[0] + "_" + vCol[1]]
            self.PRACenter.AddFeature(vCol[0] + "_" + vCol[1], "q")
        return True
    
    def ReadRwFname(self,RwFnameIn):
        lFNameWithLvl = []
        for line in open(RwFnameIn):
            vCol = line.strip().split()
            lFNameWithLvl.append([vCol[0],int(vCol[1])])
        lFNameWithLvl.sort(key=itemgetter(1))
        for FName in lFNameWithLvl:
            self.lRwFName.append(FName[0])
        return True
    
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.OutName = conf.GetConf("out")
        self.ReadQid(conf.GetConf('in'))
        self.ReadRwFname(conf.GetConf('rwfname'))
        return True
    
    def __init__(self,ConfIn = ""):
        self.Init();
        if "" != ConfIn:
            self.SetConf(ConfIn)
        return
    
    
    def ProcessOneObj(self,RwNode):
        #check if this object has required start node
        if not RwNode.ObjId in self.hObjStNode:
            return []  
        print "process [%s]" %(RwNode.ObjId)             
#         lStPRA = self.hObjPRA[RwNode.ObjId]        
        self.AddPRA(RwNode)
        self.AddStNode(RwNode)
        lTermWithFeature = self.GenerateExpTerm(RwNode)    
        print "[%s] expand [%d] terms" %(RwNode.ObjId,len(lTermWithFeature))
#         for term in lTermWithFeature:
#             print "term [%s] feature [%s]" %(term[0],term[1])          
        return lTermWithFeature
    
    
    def AddPRA(self,RwNode):        
        for edge in RwNode.lEdge:
            EdgeName = DiscardPrefix(edge[0])
            EdgeObj = edge[1]
            if EdgeObj == RwNode.ObjId:
                continue
            lStStr = []
            if RwNode.ObjId in self.PRACenter.hObjPRA:
                lStStr = self.PRACenter.hObjPRA[RwNode.ObjId]
            self.NewPRACenter.AddFeature(EdgeObj, EdgeName, lStStr)
        return True
    
    def AppendEdgeTolPRA(self,lStPRA,EdgeName):
        lRes = []
        for pra in lStPRA:
            lRes.append(pra + '#' + EdgeName)
        return lRes
    
    def AddStNode(self,RwNode):
        #for all connected node, add this obj's start nodes to theirs
        lStNode = self.hObjStNode[RwNode.ObjId]
        for Edge in RwNode.lEdge:
            ObjId = Edge[1]
            if not ObjId in self.hObjStNode:
                self.hNewObjStNode[ObjId] = lStNode
            else:
                self.hNewObjStNode[ObjId] = self.UniqAddToList(lStNode, self.hObjStNode[ObjId])
        return True
                
        
        
    def UniqAddToList(self,ListA,Target):
        for item in ListA:
            if not item in Target:
                Target.append(item)
        return Target
                
    
    def GenerateExpTerm(self,RwNode):
        lTermWithFeature = []
        for Att in RwNode.lAtt:
            AttName = Att[0]
            text = ""
            if len(Att) > 1:
                text = Att[1]
            lStPRA = self.PRACenter.GetPRAStr(RwNode.ObjId)
            lTermPRA = self.AppendEdgeTolPRA(lStPRA,AttName)
#             print "[%d] st pra str in exp term" %(len(lStPRA))
            text = DiscardStopWord(text)
            if "" == text:
                continue
            for term in text.split():
                term = DiscardNonAlphaNonDigit(term.lower())
                lTermWithFeature.append([term,self.MakeTermPRAFeatureString(lTermPRA)])              
        return lTermWithFeature
    
    def MakeTermPRAFeatureString(self,lTermPRA):
        hPRA = {}
        for pra in lTermPRA:
            if not pra in hPRA:
                hPRA[pra] = 0
#                 print 'new f [%s]' %(pra)
            hPRA[pra] += 1
        res = ""
        for item in hPRA:
            res += item + '&%d' %(hPRA[item]) + ','
        return res.strip()
    
    def Process(self):
        #for each file
        #read object, check if is in hReqQid
        #call ProcessOneObj
        #output
        
        #first make New and Old the same
        self.NewPRACenter = copy.deepcopy(self.PRACenter)
        self.hNewObjStNode = copy.deepcopy(self.hObjStNode)
        out = open(self.OutName,'w')
        for fname in self.lRwFName:
            print "start in file [%s]" %(fname)                    
            for line in open(fname):
                line = line.strip()
                RwNode = FbRwNodeC(line) 
#                 if not RwNode.Qid in self.hReqQid:
#                     continue                
                lTermWithFeature = self.ProcessOneObj(RwNode)       
                #return results should be different                      
                for term in lTermWithFeature:
                    for StNode in self.hObjStNode[RwNode.ObjId]:
                        Qid,query = StNode.split('_')
                        print >>out,Qid + "\t" + query + '\t' + term[0] + '\t' + term[1]
            self.PRACenter = copy.deepcopy(self.NewPRACenter)    
            self.hObjStNode = copy.deepcopy(self.hNewObjStNode)
        out.close()        
        return True             
                
                
                
                
                
                
                
                
                
                
                 
            