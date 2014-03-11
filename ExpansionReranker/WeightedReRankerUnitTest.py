'''
Created on Mar 11, 2014
unit test of WeightedReRanker
@author: cx
'''



import sys
from WeightedReRanker import *


if 2 != len(sys.argv):
    print "1 para:conf\nin\nout\ncashdir\nnumofrerankdoc\nctfpath\nworig"
    sys.exit()
    
    
WeightedReRankerUnitTest(sys.argv[1])
print "done"
