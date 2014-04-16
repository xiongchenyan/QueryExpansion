'''
Created on Apr 16, 2014
in: exp term
out: combined indri query, one per line
@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from base.ExpTerm import *


def MakeExpQFile(llExpTerm,OutName,ExpTermNum = 10000):
    out = open(OutName,'w')
    for lExpTerm in llExpTerm:
        query = GenerateIndriExpQuery(lExpTerm,ExpTermNum)
        print >>out, query
    out.close()
    return True
