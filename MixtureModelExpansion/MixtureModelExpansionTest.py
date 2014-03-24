'''
Created on Mar 23, 2014

@author: cx
'''
from MixtureModelExpansion import *

import sys


if 2 != len(sys.argv):
    print "1 para conf"
    MixtureModelExpansionC.ShowConf()
    sys.exit()
    
    
MixtureModelExpansionUnitTest(sys.argv[1])
print "done"



    