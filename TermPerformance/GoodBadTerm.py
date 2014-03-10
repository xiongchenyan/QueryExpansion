'''
Created on Feb 19, 2014
score = TermScore - OriginalScore
count best Score
@author: cx
'''


import sys


if 3 != len(sys.argv):
    print "2 para: term score + output"
    sys.exit()
    
out = open(sys.argv[2],'w')

hQT = {}

for line in open(sys.argv[1]):
    vCol = line.strip().split('\t')
    score = float(vCol[4]) - float(vCol[3])
    qid = vCol[0]
    query = vCol[1]
    key = qid + "_" + query
    if not (key) in hQT:
        hQT[key] = [0,0,0]
    if score > 0.001:
        hQT[key][0] += 1
        continue
    if score < -0.001:
        hQT[key][2] += 1
        continue
    hQT[key][1] += 1
    
GoodCnt = 0
NormalCnt = 0
BadCnt = 0    
for item in hQT:
    qid,query = item.split('_')
    Good,Med,Bad = hQT[item]
    print >> out,qid + '\t' + query + '\t%d\t%d\t%d' %(Good,Med,Bad)
    GoodCnt += Good
    NormalCnt += Med
    BadCnt += Bad
    
out.close()
print '%s\t%d\t%d\t%d\n' %(sys.argv[1],GoodCnt,NormalCnt,BadCnt)
