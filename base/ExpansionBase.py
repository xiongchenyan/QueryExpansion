'''
Created on Mar 7, 2014
the base class (general class) for query expansion
implement the APIs, initialization, and pre load recourses
@author: cx
'''


'''
Input: query, + lPackedIndriRes
output: lExpTerm
conf:
    path to to load resources (CTF, etc)
    parameter values
'''



import site
site.addsitedir('/bos/usr4/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr4/cx/cxPylib')

from IndriRelate.IndriPackedRes import *
from IndriRelate.CtfLoader import *
from ExpTerm import *
from cxBase.base import cxConf
from IndriRelate.IndriInferencer import *

class QueryExpansionC:
    
    def Init(self):
   #     self.WOrig = 0.5
        self.DirMu = 0
        self.NumOfExpTerm = 10
        self.PrfDocNum = 10
        self.CtfCenter = TermCtfC()
        return
    
    def __init__(self,ConfIn = ""):
        self.Init()
        if ConfIn != "":
            self.SetConf(ConfIn)
        return
    
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
    #    self.WOrig = float(conf.LoadConf("worig"))
        self.DirMu = float(conf.GetConf('dirmu'))
        self.NumOfExpTerm = float(conf.GetConf("numofexpterm"))
        self.PrfDocNum = int(conf.GetConf('prfdocnum'))
        self.CtfCenter.Load(conf.GetConf("ctfpath"))
        return True
    
    def ShowConf(self):
        print "dirmu\nnumofexpterm\nctfpath"
        return True
    
    
    
    def Process(self,qid,query,lDoc):
        print "call my sub class's process"
        print "input:query + list of docs\noutput: a list of exp terms"
        return False
    
    
    def NormalizeExpTermWeight(self,lExpTerm):
        Z = 0
        for expterm in lExpTerm:
            Z += expterm.score
        for i in range(len(lExpTerm)):
            lExpTerm[i] /= Z
        return True
    
        
        



 
