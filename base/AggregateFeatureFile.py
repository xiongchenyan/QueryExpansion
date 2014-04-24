'''
Created on Apr 23, 2014
agrregate a feature file of exp term
input:sorted exp term feature qid\tquery\texpterm\t score \t features
do: merge feature of a q-t, (sorted to appear together)
output: exp term, with feature ready
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

from cxBase.KeyFileReader import KeyFileReaderC
from base.ExpTerm import ExpTermC
import sys
if 3 != len(sys.argv):
    print "2 para: term feature in + output"
    sys.exit()
    
    
out = open(sys.argv[2],'w')


KeyReader = KeyFileReaderC()

KeyReader.open(sys.argv[1])

for lvCol in KeyReader:
    ExpTerm = ExpTermC()
    for vCol in ExpTerm:
        Mid = ExpTermC('\t'.join(vCol))
        if ExpTerm.empty():
            ExpTerm = Mid
        else:
            ExpTerm.AddFeature(Mid.hFeature)
    print "[%s] done" %(ExpTerm.Key())
    print >> out, ExpTerm.dump()
    
out.close()
    
