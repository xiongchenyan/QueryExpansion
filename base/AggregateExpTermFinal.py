'''
Created on May 6, 2014
final one
@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
import sys
from ExpTerm import *
from copy import deepcopy

from operator import attrgetter
from cxBase.base import cxConf

def LoadAndMergeOneExpTerm(InName):
    #read file, hash them, and add features one by one
    hExpTerm = {} #key->exp term
    
    for line in open(InName):
        ExpTerm = ExpTermC(line.strip())
        if ExpTerm.Key() in hExpTerm:
            hExpTerm[ExpTerm.Key()].AddFeature(ExpTerm.hFeature)
        else:
            hExpTerm[ExpTerm.Key()] = ExpTerm
    return hExpTerm


def MergeFilesToADict(hExpTerm,lInName,Intersect=True):
    #if Intersect, then only keep those appear in both
    #else keep those appear in hExpTerm
    hIntersect = {}
    
    for InName in lInName:
        print "mergeing [%s]" %(InName)
        for line in open(InName):
            ExpTerm = ExpTermC(line.strip())
            if ExpTerm.Key() in hExpTerm:
                hIntersect[ExpTerm.Key()] = True
                hExpTerm[ExpTerm.Key()].AddFeature(ExpTerm.hFeature)
    
    hResExp = {}
    if not Intersect:
        hResExp = deepcopy(hExpTerm)
    else:
        for item in hIntersect:
            hResExp[item] = deepcopy(hExpTerm[item])
    return hResExp



if 2 != len(sys.argv):
    print "conf:"
    print "target\nmergefile\nintersect 1\nout"
    sys.exit()
    
conf = cxConf(sys.argv[1])
TargetIn = conf.GetConf('target')
lInName = conf.GetConf('mergefile')
OutName = conf.GetConf('out')
if type(lInName) == str:
    lInName = [lInName]
Intersect = bool(int(conf.GetConf('intersect',1)))

hExpTerm = LoadAndMergeOneExpTerm(TargetIn)
hResExp = MergeFilesToADict(hExpTerm,lInName,Intersect)

lExpTerm = [ExpTerm for key,ExpTerm in hResExp.items()]
lExpTerm.sort(key=attrgetter('qid'))

out = open(OutName,'w')
for ExpTerm in lExpTerm:
    print >>out,ExpTerm.dump()
    
out.close()
    
    

