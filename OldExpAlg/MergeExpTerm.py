'''
Created on Feb 17, 2014
merge expansion terms
input: each line is a ExpTerm.dump, sorted
read them and merge them
output: merged terms
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr0/cx/cxPylib')
site.addsitedir('/bos/usr0/cx/PyCode/KnowledgeBase')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
from cxBase.base import *
from base.ExpTerm import *
# from operator import itemgetter


import sys
import copy


def MergeTerm(lExpTerm):
    print "start merge [%d] term" %(len(lExpTerm))
    ResTerm = copy.deepcopy(lExpTerm[0])
#     print "init [%s]" %(ResTerm.dump())
    for i in range(1,len(lExpTerm)):
        ResTerm.AddFeature(lExpTerm[i].hFeature)
#         print "add feature [%s]" %(ResTerm.dump())
    return ResTerm


if 3 != len(sys.argv):
    print "2 para: input (sortted to merge term) + output"
    sys.exit()
    
    
CurrentKey = ""
out = open(sys.argv[2],'w')
lExpTerm = []
for line in open(sys.argv[1]):
    ExpTerm =  ExpTermC(line.strip())
    key = ExpTerm.Key()
    if CurrentKey == "":
        CurrentKey = key
    if CurrentKey != key:
        print "merging key [%s]" %(CurrentKey)
        ResTerm = MergeTerm(lExpTerm)
        print >> out,ResTerm.dump()
#         print "get [%s]" %(ResTerm.dump())
        CurrentKey = key
        lExpTerm = []
    lExpTerm.append(ExpTerm)
ResTerm = MergeTerm(lExpTerm)
print >> out,ResTerm.dump()

out.close()


