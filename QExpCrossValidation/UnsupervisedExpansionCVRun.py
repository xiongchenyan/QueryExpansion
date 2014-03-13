'''
Created on Mar 12, 2014
run unsupervisedexpansioncv
@author: cx
'''

from UnsupervisedExpansionCV import *

import sys

if 2 != len(sys.argv):
    print "1 para conf:\ncashdir\nin\nevaoutdir\nctfpath\nparaset\nqrel\nevadepth\nworig\nnumofexpterm\ndirmu\nprfdocnum\nk"
    sys.exit()
    
    
ExpansionCV = UnsupervisedExpansionCVC(sys.argv[1])

ExpansionCV.Process()

print "finished"