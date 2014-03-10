'''
Created on Feb 19, 2014
discard noise expansion terms (pra)
rule1: vCol[3] or later has space, then discard
rule2: has space in term, or pure digits.
@author: cx
'''


import sys
import site
site.addsitedir('/bos/usr0/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr0/cx/cxPylib')
from cxBase.base import *

def DiscardErrPRA(vCol):
    for i in range(3,len(vCol)):
        if ' ' in vCol[i]:
            return True
    return False

def DiscardSpace(vCol):
    lMid = vCol[2].split()
    if len(lMid) > 1:
        return True
    return False

def DiscardDigit(vCol):
    term = DiscardNonAlpha(vCol[2]).replace(' ','')
    if "" == term:
        return True
    return False

if 3 != len(sys.argv):
    print "2para: input + filtered out"
    sys.exit()
    
    
out = open(sys.argv[2],'w')
FilterOut = open(sys.argv[2] + '_filter','w')
for line in open(sys.argv[1]):
    line = line.strip()
    vCol = line.split('\t')
    if not(DiscardErrPRA(vCol) | DiscardSpace(vCol) | DiscardDigit(vCol)):
        vCol[2] = vCol[2].replace(' ','')
        print >> out, '\t'.join(vCol)       
        
out.close()
FilterOut.close()
    





