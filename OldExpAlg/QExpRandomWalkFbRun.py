'''
Created on Feb 13, 2014
run QExp
@author: cx
'''

from QExpRandomWalkFb import *

import sys

if 2 != len(sys.argv):
    print "1para: conf\nin\nout\nrwfname"
    sys.exit()
    
QExpRw = QExpRandomWalkFbC(sys.argv[1])
QExpRw.Process()

print "done"
