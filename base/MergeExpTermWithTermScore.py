'''
Created on Feb 18, 2014
merge ExpTerm with TermScore
TermScore File:
    output of SingleTermGain (I didn't use ExpTerm output in SingleTermGain for flexibility)
output:
    Expterm format, with score
        currently score is: Term Exp Score - original score
@author: cx
'''




import site
site.addsitedir('/bos/usr4/cx/local/lib/python2.7/site-packages')
site.addsitedir('bos/usr4/cx/PyCode/QueryExpansion')
from base.ExpTerm import *
import sys


def GenerateScore(OriginalScore,TermScore):
    return TermScore - OriginalScore

def ReadQTermScore(ScoreInName):
    hQTermScore = {}
    for line in open(ScoreInName):
        vCol = line.strip().split('\t')
        qid = vCol[0]
        query = vCol[1]
        term = vCol[2]
        OriginalScore = float(vCol[3])
        TermScore = float(vCol[4])
        score = GenerateScore(OriginalScore,TermScore)
        hQTermScore[qid+'_' + query+'_'+term] = score
    return hQTermScore



if 4 != len(sys.argv):
    print "3para: exp term + term score + output"
    sys.exit()
    


hQTermScore = ReadQTermScore(sys.argv[2])
out = open(sys.argv[3],'w')

for line in open(sys.argv[1]):
    line = line.strip()
    ExpTerm = ExpTermC(line)
    key = ExpTerm.Key()
    if key in hQTermScore:
        ExpTerm.score = hQTermScore[key]
    print >>out, ExpTerm.dump()
    
out.close()
print "done"    

