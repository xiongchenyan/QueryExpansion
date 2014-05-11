'''
Created on Feb 17, 2014
data structure for expansion terms
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

import json,math
from json import JSONEncoder
from FreebaseDump.FbDumpBasic import GetDomain
from cxBase.FeatureBase import cxFeatureC
from copy import deepcopy
class ExpTermC(cxFeatureC):
    
    def Init(self):
        super(ExpTermC,self).Init()
        self.term = ""
        self.query = ""
        self.qid = ""
        self.score = 0
        
        

    
    
    def loads(self,line):
        self.load(line)
        
    def load(self,line):
#         print "loading exp term line [%s]" %(line)
        vCol = line.strip().split('\t')
        if len(vCol) < 3:
            print "%s format error" %(line)
            return False
#         print json.dumps(vCol)
        self.qid = vCol[0]
        self.query = vCol[1]
        self.term = vCol[2]
        if len(vCol) > 3:
            self.score = float(vCol[3])            
        if len(vCol) > 4:
            super(ExpTermC,self).loads('\t'.join(vCol[4:]))
        return True
    
    
    
    
    def dumps(self):
        return self.dump(
                         )    
    def dump(self):
        line = self.qid + "\t" + self.query + '\t' + self.term + '\t%f'%(self.score) + '\t' + super(ExpTermC,self).dumps()
         
        return line
    
    
    
    def __deepcopy__(self,memo):
        #must use the deepcopy function to make sure memo is correct?
        Term = ExpTermC()
        Term.term = deepcopy(self.term,memo)
        Term.query = deepcopy(self.qid,memo)
        Term.qid = deepcopy(self.query,memo)
        Term.score = deepcopy(self.score,memo)
        Term.hFeature = deepcopy(self.hFeature,memo)
        return Term

    def Key(self):
        return self.qid + "_"  +self.query + "_" + self.term
    
    
    def IsEmpty(self):
        return self.Key() == ExpTermC().Key()
    
    def empty(self):
        return self.IsEmpty()
    
    
    
                    
    @staticmethod    
    def FilterNonPosFeature(lData):
        #can only be done on training data
        hFeature = {}
        for data in lData:
            if data.score <= 0:
                continue
            hFeature.update(data.hFeature)
        print "filter non pos feature in training, [%d] left" %(len(hFeature))
        lNew = []
        for data in lData:
            hNew = {}
            for feature in data.hFeature:
                if feature in hFeature:
                    hNew[feature] = data.hFeature[feature]
            data.hFeature.clear()
            data.hFeature = hNew
            lNew.append(data)
        return lNew 
            
    @staticmethod
    def SplitByQid(lExpTerm):
        #lExpterm must be sortted
        llExpTerm = [[]]
        p = 0
        CurrentQid = -1
        for ExpTerm in llExpTerm:
            if CurrentQid == -1:
                CurrentQid = ExpTerm.qid
            if CurrentQid != ExpTerm.qid:
                llExpTerm.append([])
                p += 1
            llExpTerm[p].append(ExpTerm)
        return llExpTerm
            
        
        
        
        
        
        
        
    
    @staticmethod
    def IsPRAFeature(feature):
#         print "check [%s] whether PRA" %(feature)
        try:
            l = json.loads(feature)
#             print "loaded l [%s]" %(json.dumps(l))
            if type(l) == list:
                return True
            return False
        except ValueError:
            return False
    @staticmethod
    def IsPRFFeature(feature):
        lPRF = ["CooccurSingleQTermPRF",
                "CooccurSingleQTermCorp",
                "TermDistCorp",
                "WeightedTermProximityCorp",
                "DocFreqCoorPSF",
                "WeightedTermProximityPRF",
                "DocFreqCoorCorp",
                "CooccurPairQTermPRF",
                "CooccurPairQTermCorp",
                "TermDistPSF"]
        if feature in lPRF:
            return True
        return False
    
    @staticmethod
    def IsWord2VecFeature(feature):
        return feature == "word2vecsim"
    
    @staticmethod
    def IsHyperEdgeFeture(feature):
        #well TBD better
        if not (ExpTermC.IsPRAFeature(feature) | ExpTermC.IsPRFFeature(feature) |
                ExpTermC.IsWord2VecFeature(feature)):
            return True
        return False
    @staticmethod
    def FeatureGroup(feature):
        if ExpTermC.IsPRAFeature(feature):
            return 'pra' + ExpTermC.PRAPathFeatureTypeLvl(feature)
        if ExpTermC.IsPRFFeature(feature):
            return 'prf'
        if ExpTermC.IsWord2VecFeature(feature):
            return 'word2vec'
        if ExpTermC.IsHyperEdgeFeture(feature):
            return 'hyper'
        return 'none'
        
            
        
    @staticmethod
    def PRAFeatureType(feature,Grouping='lvltype'):
        if not ExpTermC.IsPRAFeature(feature):
            return ExpTermC.FeatureGroup(feature)
        
        if Grouping == 'lvltype':
            return ExpTermC.PRAPathFeatureTypeLvlType(feature)
        if Grouping == 'type':
            return ExpTermC.PRAPathFeatureTypeType(feature)
        if Grouping == 'lvl':
            return ExpTermC.PRAPathFeatureTypeLvl(feature)
        if Grouping == 'one':
            return ExpTermC.PRAPathFeatureTypeOne(feature)
        if Grouping == 'lvltypedomain':
            return ExpTermC.PRAPathFeatureTypeLvlTypeDomain(feature)
        return ''
            
    @staticmethod
    def PRAPathFeatureTypeLvlType(feature):
        TypeStr = ''
        for edge in json.loads(feature):
            EdgeType = ExpTermC.EdgeType(edge)
            if '' == EdgeType:
                continue
            TypeStr += EdgeType + '-'
        TypeStr = TypeStr.strip('-')
#         print "[%s] type [%s]" %(feature,TypeStr)
        
        return TypeStr
    
    @staticmethod
    def PRAPathFeatureTypeType(feature):
        TypeStr = "None" #cotype, link, mix
        CotypeCnt = 0
        LinkCnt = 0
        for edge in json.loads(feature):
            EdgeType = ExpTermC.EdgeType(edge)
            if '' == EdgeType:
                continue
            if EdgeType == 'cotype':
                CotypeCnt += 1
            if EdgeType == 'link':
                LinkCnt += 1
        if (CotypeCnt > 0) & (LinkCnt > 0):
            TypeStr = 'mix'
        else:
            if CotypeCnt > 0:
                TypeStr = 'cotype'
            if LinkCnt > 0:
                TypeStr = 'link'
        return TypeStr
    
    @staticmethod
    def PRAPathFeatureTypeOne(feature):
        return ""
    
    @staticmethod
    def PRAPathFeatureTypeLvl(feature):
        TypeStr = "None"   #lvl1, lvl2
        cnt = 0
        for edge in json.loads(feature):
            EdgeType = ExpTermC.EdgeType(edge)
            if '' == EdgeType:
                continue
            cnt += 1
        TypeStr = 'Lvl%d' %(cnt)
        return TypeStr
    
    @staticmethod
    def PRAPathFeatureTypeLvlTypeDomain(feature):
        TypeStr = ""   #type-domain-type-domain
        for edge in json.loads(feature):
            if type(edge) == list:
                edge = edge[0]            
            Domain = GetDomain(edge)
            TypeStr += Domain + '-'
        TypeStr = TypeStr.strip('-')
        return ""
        
        
        
    @staticmethod
    def EdgeType(edge):
        lStop = set(['search','desp','name'])
        if edge in lStop:
            return ''
        if 'cotype' in edge:
            return 'cotype'
        return 'link'
            
        
hStopEdge = dict(zip(['search','desp','name'],range(4)))
    
def SegEdgeFromPRAFeature(feature,DiscardStop = False):
    lPath = json.loads(feature)
    lEdge = []
    for item in lPath:
        lEdge.append(str(item))
    if DiscardStop:
        lEdge = [edge for edge in lEdge if not edge in hStopEdge]
    return lEdge


def ReadQExpTerms(InName):
    #read expansion terms from in name
    #group by qid
    llExpTerm = []
    
    p = 0
    llExpTerm.append([])
    for line in open(InName):
        line = line.strip()
        ExpTerm = ExpTermC(line)
        if llExpTerm[p] != []:
            if ExpTerm.qid != llExpTerm[p][0].qid:
                llExpTerm.append([])
                p += 1
        llExpTerm[p].append(ExpTerm)
    return llExpTerm 
    
def DumpQExpTerms(llExpTerm,OutName):
    out = open(OutName,'w')
    for lExpTerm in llExpTerm:
        for ExpTerm in lExpTerm:
            print >>out, ExpTerm.dump()
    out.close()
    return True


def BinarizeScore(lExpTerm,Thre = 0):
    for i in range(len(lExpTerm)):
        if lExpTerm[i].score > Thre:
            lExpTerm[i].score = 1
        else:
            lExpTerm[i].score = 0
    return lExpTerm
    
    
def SplitQidQuery(llExpTerm):
    lQid = []
    lQuery = []
    for lExpTerm in llExpTerm:
        lQid.append(lExpTerm[0].qid)
        lQuery.append(lExpTerm[0].query)
    return lQid,lQuery
    
    
def MinMaxFeatureNormalize(lExpTerm):
    #get min max for each feature dimension
    hMin = {}
    hMax = {}
    for ExpTerm in lExpTerm:
        for feature in ExpTerm.hFeature:
            value = ExpTerm.hFeature[feature]
            if not feature in hMin:
                hMin[feature] = value
            if not feature in hMax:
                hMax[feature] = value
            hMin[feature] = min(hMin[feature],value)
            hMax[feature] = max(hMax[feature],value)
    
    
    #min-max normalization
    #if min==max then set to 0
    
    for i in range(len(lExpTerm)):
        for feature in lExpTerm[i].hFeature:
            fMin = hMin[feature]
            fMax = hMax[feature]
            
            if fMin == fMax:
                lExpTerm[i].hFeature[feature] = 0
                continue
            lExpTerm[i].hFeature[feature] = (lExpTerm[i].hFeature[feature] - fMin)/(fMax - fMin)
    
    return True
            
            
            
def SplitLabelAndFeature(llExpTerm,BinaryScore = False):
    #generate label (y) and lhFeature (x)
    lScore = []
    lhFeature = []
    for lExpTerm in llExpTerm:
        for ExpTerm in lExpTerm:
            score = ExpTerm.score
            if BinaryScore:
                if score > 0:
                    score = 1
                else:
                    score = 0
            lScore.append(score)            
            hFeature = {}
            for item in ExpTerm.hFeature:
                hFeature[int(item)] = ExpTerm.hFeature[item]
            lhFeature.append(hFeature)
    return lScore,lhFeature
        
    
    
def NormalizeExpTermWeight(lExpTerm):
    Z = 0
    for expterm in lExpTerm:
        Z += expterm.score
    if Z != 0:
        for i in range(len(lExpTerm)):
            lExpTerm[i].score /= Z
    else:
        if lExpTerm != []:
            print "exp term for q [%s] all zero" %(lExpTerm[0].query)
    return lExpTerm    
    
    

def GenerateIndriExpQuery(lExpTerm,NumOfExpTerm = 10000):
    #generate default indri expansion query
    #lExpterm should be for a same query (off course)
    lExpTerm = lExpTerm[:NumOfExpTerm]
    WOrig = 0.5
    if len(lExpTerm) == 0:
        return ""
    query = lExpTerm[0].query
    
    ExpQuery = '#weight(%f #combine (%s) ' %(WOrig,query)
    QNew = "#weight("
    for ExpTerm in lExpTerm:
        QNew += " %f %s" %(ExpTerm.score,ExpTerm.term)
    QNew += ")"
    
    ExpQuery += "%f %s)" %(1-WOrig,QNew)
    return ExpQuery
        
        
    
    
    
        
    
    
    

