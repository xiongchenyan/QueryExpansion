'''
Created on Nov 20, 2013
base func class for expansion terms
@author: cx
'''



class WTermC:
    qid=0
    query=""
    term=""
    weight=0
    rank=-1
    def __init__(self,line=""):
        self.Init()
        if line != "":
            self.set(line)
        return       
    def Init(self):
        self.qid=0
        self.query = 0
        self.term = ""
        self.weight = 0
        self.rank = -1
        return
    def set(self,line):
        vCol = line.strip().split("\t")
        if len(vCol) != 4:
            print "%s format errof col != 4" %(line)
        self.qid = int(vCol[0])
        self.query = vCol[1]
        self.term = vCol[2]
        self.weight = float(vCol[3])
        return True
    def out(self):
        return str(self.qid) + "\t" + self.query + "\t" + self.term + "\t" + str(self.weight)
    
    
def LoadWTermFile(InName):
    lWTerm = []
    LastQid = -1
    rank = 1
    for line in open(InName):
        line = line.strip()
        wterm = WTermC(line)
        qid = wterm.qid
        if qid != LastQid:
            rank = 1            
            LastQid = qid
        wterm.rank = rank
        rank += 1
        lWTerm.append(wterm)
    print "load [%d] term from [%s]" %(len(lWTerm),InName)
    return lWTerm

def OutlWTerm(OutName,lWTerm):
    out = open(OutName,"w")
    for wterm in lWTerm:
        print >> out, wterm.out()
    out.close()
    



def ReformlWTerm(lMergeWTerm,qid,query):
    lFinalWTerm = []
    for term in lMergeWTerm:
        WTerm = WTermC();
        WTerm.qid = qid;
        WTerm.query = query;
        WTerm.term = term[0]
        WTerm.weight = term[1]
        lFinalWTerm.append(WTerm)
    return lFinalWTerm

def SplitlWTermsByQid(lWTerm):
    llWTerm = []
    hQidPos = {}
    LastQid = -1
    Pos = -1
    for wterm in lWTerm:
        if wterm.qid != LastQid:
            Pos += 1
            hQidPos[wterm.qid] = Pos
            llWTerm.append([])
            LastQid = wterm.qid
        llWTerm[Pos].append(wterm)
    return llWTerm,hQidPos
    

def MakeRankMap(lWTerm):
    hRankMap = {}
    for wterm in lWTerm:
        hRankMap[wterm.term] = wterm.rank
    return hRankMap
        