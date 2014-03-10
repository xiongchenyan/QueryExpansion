'''
Created on Feb 17, 2014
transfer to query node. from output of DirectSearchGoogleAPI
@author: cx
'''

import site
site.addsitedir('/bos/usr4/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr4/cx/cxPylib')
site.addsitedir('/bos/usr4/cx/PyCode/KnowledgeBase')
from cxBase.base import cxConf
from FreebaseRandomWalk.FbRwNode import *


EdgeName = "init"

def TransferPerQ(lvCol):
    RwNode = FbRwNodeC()
    RwNode.ObjId = lvCol[0][0] + "_" + lvCol[0][1]
    global EdgeName
    for vCol in lvCol:
        RwNode.lEdge.append([EdgeName,vCol[2]])
    RwNode.lAtt.append(['init',''])
    return RwNode


if 2 != len(sys.argv):
    print "1 para: conf:\nedgename\nin\nout\ntopnobj"
    sys.exit()
    
    
conf = cxConf(sys.argv[1])

InName = conf.GetConf("in")
OutName = conf.GetConf('out')
EdgeName = conf.GetConf('edgename')
TopN = int(conf.GetConf('topnobj'))


out = open(OutName,'w')
ThisQid = ""
lvCol = []
for line in open(InName):
    vCol = line.strip().split('\t')
    CurrentQid = vCol[0]
    if ThisQid == "":
        ThisQid = CurrentQid
    if CurrentQid != ThisQid:
        if len(lvCol) > TopN:
            lvCol = lvCol[0:TopN]
        RwNode = TransferPerQ(lvCol)
        print >> out, RwNode.Dump()
        lvCol = []
        ThisQid = CurrentQid
    lvCol.append(vCol)
    
if len(lvCol) > TopN:
    lvCol = lvCol[0:TopN]
RwNode = TransferPerQ(lvCol)
print >> out, RwNode.Dump()

out.close()
print "finish"