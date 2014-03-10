'''
Created on Feb 11, 2014
using top results from Google
input: qid\tquery
output: qid\tquery\tobject\tlvl(0 always)
@author: cx
'''



import site
site.addsitedir('/bos/usr4/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr4/cx/cxPylib')
from FreebaseRelate.SearchApiFetcher import *
import sys
if 3 != len(sys.argv):
    print "2 para: queries + output"
    sys.exit()
    
    
out = open(sys.argv[2],'w')
for line in open(sys.argv[1]):
    vCol = line.strip().split('\t')
    qid = vCol[0]
    query = vCol[1]
    lObj = FetchFbObjFromGoogleAPI(query)
    for Obj in lObj:
        print >>out, "%s\t%s\t%s\t0" %(qid,query,Obj.ObjId)
        
out.close()

