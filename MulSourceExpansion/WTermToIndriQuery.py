'''
Created on Nov 20, 2013
generate indri query from wterm
@author: cx
'''


from ExpansionTermBase import *
import sys
import json
ExpansionWeight = 0.5
MaxExpTermNum = 10
def MakeIndriQ(lWTerm):
    qid = lWTerm[0].qid
    query = lWTerm[0].query
    CombQuery = "#weight( %f #combine( %s ) %f #weight( " %(1-ExpansionWeight, query, ExpansionWeight)
    cnt = 0
    for wterm in lWTerm:
        CombQuery += "%f \"%s\" " %(wterm.weight,wterm.term)
        cnt += 1
        if cnt >= MaxExpTermNum:
            break        
    CombQuery += ") )\t%d" %(qid)
    return CombQuery


if 3 != len(sys.argv):
    print "2 para: wterms + outname (indri query)"
    sys.exit()
    
lWTerm = LoadWTermFile(sys.argv[1])
llWTerm,hQid = SplitlWTermsByQid(lWTerm)
# print "split to [%d] qid" %(len(llWTerm))
out = open(sys.argv[2],'w')
for QWTerm in llWTerm:
#     print "reforming [%d]" %(QWTerm[0].qid)
    print >> out,MakeIndriQ(QWTerm)
    
out.close()