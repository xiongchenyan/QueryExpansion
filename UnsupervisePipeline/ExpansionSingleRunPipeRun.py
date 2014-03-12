'''
Created on Mar 12, 2014
run ExpansionSingleRun
@author: cx
'''

from ExpansionSingleRunPipe import *


import sys


if 2 != len(sys.argv):
    print "1 para: conf\ncashdir\nin\nevaoutdir\nctfpath\nparaset\nqrel\nevadepth\nworig\nnumofexpterm\ndirmu\nprfdocnum\n"
    sys.exit()
    
    
SingleRunPipe = ExpansionSingleRunPipeC(sys.argv[1])
SingleRunPipe.Process()
BestMapP,BestNdcgP,BestErrP = SingleRunPipe.PickBestParaSet()

print "best map para [%s][%f]" %(SingleRunPipe.lParaSet[BestMapP].dumps(),SingleRunPipe.lEvaRes[BestMapP].map)
print "best ndcg para [%s][%f]" %(SingleRunPipe.lParaSet[BestNdcgP].dumps(),SingleRunPipe.lEvaRes[BestNdcgP].ndcg)
print "best err para [%s][%f]" %(SingleRunPipe.lParaSet[BestErrP].dumps(),SingleRunPipe.lEvaRes[BestErrP].err)
