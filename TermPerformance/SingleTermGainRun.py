'''
Created on Feb 18, 2014
run single term gain
@author: cx
'''

from SingleTermGain import *


if 2 != len(sys.argv):
    print "1 para: conf"
    print "in\nout\nindriresdir\nnewtermweight\nctf\nqrel\nevadepth"
    sys.exit()
    
    
SingleTermGain = SingleTermGainC(sys.argv[1])
SingleTermGain.EvaluateFile()

print "done"
