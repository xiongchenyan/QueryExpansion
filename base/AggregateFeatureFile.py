'''
Created on Apr 9, 2014
aggregate feature file for exp term
input 1: q exp term file (with score, etc ready)
input 2: sorted exp term feature file (key could be multiple appearance, but must be together)
do:
    merge features in feature file to exp term (count is added)
    and output statistic informations
        coverage of pos/neg terms in feature file for now
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

import sys
from ExpTerm import *
from copy import deepcopy
#build key->expterm
def LoadScoreExpTerm(InName):
    hExpTerm = {}
    for line in open(InName):
        ExpTerm = ExpTermC(line)
        hExpTerm[ExpTerm.Key()] = ExpTerm
    return hExpTerm



if 4 != len(sys.argv):
    print "score term + feature term file + output"
    sys.exit()
    
hExpTerm = LoadScoreExpTerm(sys.argv[1])
print "load [%d] pair" %(len(hExpTerm))
out = open(sys.argv[3],'w')

lLabelCnt = [[0,0],[0,0]]

for Term in hExpTerm:
    if hExpTerm[Term].score > 0:
        lLabelCnt[0][0] += 1
    else:
        lLabelCnt[0][1] += 1


CurrentExpTerm = ExpTermC()
for line in open(sys.argv[2]):
    line = line.strip()
    ThisExpTerm = ExpTermC(line)
    if not ThisExpTerm.Key() in hExpTerm:
        continue    
    if CurrentExpTerm.Key() == "":
        CurrentExpTerm = deepcopy(hExpTerm[ThisExpTerm.Key()])
    
    if CurrentExpTerm.Key() != ThisExpTerm.Key():
        print >>out, CurrentExpTerm.dump()
        if CurrentExpTerm.score > 0:
            lLabelCnt[1][0] += 1
        else:
            lLabelCnt[1][1] += 1
        
               
        CurrentExpTerm = deepcopy(hExpTerm[ThisExpTerm.Key()])
        
    
    CurrentExpTerm.AddFeature(ThisExpTerm.hFeature)
    
print >>out,CurrentExpTerm.dump()
if CurrentExpTerm.score > 0:
    lLabelCnt[1][0] += 1
else:
    lLabelCnt[1][1] += 1
out.close()

print "label cnt:\n%s" %(json.dumps(lLabelCnt,indent=1))

print "finished"
        
