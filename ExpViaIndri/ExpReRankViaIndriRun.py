'''
Created on Apr 16, 2014

@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from ExpReRankViaIndri import *


import sys

if 2 != len(sys.argv):
    print "1 para conf"
    ExpReRankViaIndriC().ShowConf()
    sys.exit()
    
    
ExpReRanker = ExpReRankViaIndriC(sys.argv[1])
ExpReRanker.Process()

print "finished"
