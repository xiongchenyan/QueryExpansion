'''
Created on Feb 18, 2014
select term with feature PRA len < given n
input: a file each line is a ExpTerm
output: filtered terms
@author: cx
'''

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
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
from cxBase.base import *
from base.ExpTerm import *

import sys

if 4 != len(sys.argv):
    print "3 para: expansion terms + max lvl + outname"
    sys.exit()
    
    
MaxLvl = int(sys.argv[2])
out = open(sys.argv[3],'w')

for line in open(sys.argv[1]):
    line = line.strip()
    ExpTerm = ExpTermC(line)
    ExpTerm.ExtractPRALengthFeature()
    flag = False
    for i in range(1,MaxLvl + 1):
        name = 'CntPRALen%d' %(i)
        if name in ExpTerm.hFeature:
            flag = True
            break
    if flag:
        print >> out, ExpTerm.dump()
        
        
out.close()
