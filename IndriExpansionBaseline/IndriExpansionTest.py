'''
Created on Mar 10, 2014
unit test
@author: cx
'''

from IndriExpansion import *

import sys


if 2 != len(sys.argv):
    print "1 conf:in\nout\ncashdir\nprfdocnum\ndirmu\nnumofexpterm\nctfpath"
    sys.exit()
    
    
IndriExpansionUnitTest(sys.argv[1])
print "done"



    
