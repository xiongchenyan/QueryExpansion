'''
Created on Apr 29, 2014
in: main term 1 + target term 2 + output
do: add feature in 2 to 1
@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

from cxBase.KeyFileReader import KeyFileReaderC
from base.ExpTerm import ExpTermC
import sys
if 4 != len(sys.argv):
    print "3 para: main term  + to add feature term + output"
    sys.exit()
    
    
hAddFeature = {}

for line in open(sys.argv[2]):
    ExpTerm = ExpTermC(line.strip())
    hAddFeature[ExpTerm.Key()] = ExpTerm.hFeature
    
out = open(sys.argv[3])

for line in open(sys.argv[1]):
    ExpTerm = ExpTermC(line.strip())
    if ExpTerm.Key() in hAddFeature:
        ExpTerm.AddFeature(hAddFeature[ExpTerm.Key()])
    print >>out, ExpTerm.dump()
    
out.close()
    
    
