'''
Created on Nov 20, 2013
Merge multiple input wterms using different weighting schema
@author: cx
'''


import site
site.addsitedir('/bos/usr4/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr4/cx/cxPylib')
import sys
from ExpansionTermBase import *
from RankAggregation.ReciprocalRankMerge import *


def RRMergelWTerms(llWTerm):
    #form lWTerm from each list, of same qid
    #then merge those of same qid-query's wterms
        #make {term:rank}'s
        #rr merge, call RR
        #make bakc toe WTermC
    #combine to a same lWTerm and return
    lFinalWTerm=[]    
    #dim 1 list dim 2 qid dim 3 wterm    
    lllWTerm = []
    lQidPos = []
    for lWTerm in llWTerm:
        MidllWTerm, hQidPos = SplitlWTermsByQid(lWTerm)
#         print "split to [%d] qid-lWterm" %(len(MidllWTerm))
#         for item in hQidPos:
#             print "[%d]-[%d]" %(item,hQidPos[item])        
        lllWTerm.append(MidllWTerm)
        lQidPos.append(hQidPos)
    
    for lWTerm in lllWTerm[0]:
        #just go through first list, it will contain all qid
        lhRankMap = []
        lhRankMap.append(MakeRankMap(lWTerm))
        qid = lWTerm[0].qid
        query = lWTerm[0].query
        for i in range(1,len(lllWTerm)):
            OtherListWTerm = lllWTerm[i]
            OtherListhQidPos = lQidPos[i]
            if (lWTerm[0].qid in OtherListhQidPos):
                pos = OtherListhQidPos[lWTerm[0].qid]
                OtherListThisQidWTerm = OtherListWTerm[pos]
                lhRankMap.append(MakeRankMap(OtherListThisQidWTerm))        
        #{term:rank} done in lhRankMap
#         print "start merge for [%d]" %(qid)
#         print "before merge:"
#         for hRankMap in lhRankMap:
#             lMidTerm = TransToRankList(hRankMap)
#             print "list:"
#             for term in lMidTerm:
#                 print "%s\t%f" %(term[0],term[1])
        hMergeRes = ReciprocalRankMerge(lhRankMap)
        lMergeWTerm = TransToRankList(hMergeRes)        
#         print "after merge:"
#         for term in lMergeWTerm:
#             print "%s\t%f" %(term[0],term[1])   
        lThisQWTerm = ReformlWTerm(lMergeWTerm,qid,query)
#         print "merge res for [%d]" %(qid)
#         for wterm in lThisQWTerm:
#             print wterm.out()            
        lFinalWTerm.extend(lThisQWTerm) 
#         print "now final term:"
#         for wterm in lFinalWTerm:
#             print wterm.out()       
    return lFinalWTerm

      

if 3 != len(sys.argv):
    print "2 para: a file contains input wterm files, one name per line\n + output name"
    sys.exit()
    
llWTerm = []

for line in open(sys.argv[1]):
    InName = line.strip()
    lWTerm = LoadWTermFile(InName)
    llWTerm.append(lWTerm)


    
lFinalWTerm = RRMergelWTerms(llWTerm)
OutlWTerm(sys.argv[2],lFinalWTerm)


