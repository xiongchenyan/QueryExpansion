'''
Created on Oct 2, 2013
transfer the xml file Wikipedia dump to trec web format
//url: en.wikipedia.org/wiki/ + title
//docno: wiki-ns[ns number]-[id]
read each line, discard head (until first <page> tag)
<page> and </page> tag assume occupy a single line.
read <page> to </page>, append trec web head and tail to it.
@author: cx
'''


import sys

UrlPrefix = 'http://en.wikipedia.org/wiki/'

def IsPageSt(line):
    return '<page>' == line.strip()

def IsPageEd(line):
    return '</page>' == line.strip()


def ExtractMetaInfor(PageStr):
    DocUrl = ""  
    DocNs = ''
    DocId = ''    
    vLine = PageStr.split('\n')
    for line in vLine:
        line = line.strip();
        if '' == DocUrl:
            title = SegTag(line,'title')
            if not '' == title:
                DocUrl = UrlPrefix + title
        if '' == DocNs:
            DocNs = SegTag(line,'ns')
        if '' == DocId:
            DocId = SegTag(line,'id')
    DocNo = 'wiki-ns' + DocNs + '-' + DocId
    return DocUrl,DocNo                   
    
    
def SegTag(line,tag):
    StTag = '<' + tag + ">"
    EdTag = '</' + tag + ">"
    if not StTag in line:
        return ""
    if not EdTag in line:
        return ""
    res = line.strip().replace(StTag,'').replace(EdTag,'').strip()
    return res

    
def MakeTrecWebHead(DocUrl,DocNo):
    res = "<DOC>\n<DOCNO>" + DocNo + "</DOCNO>\n"
    res += "<DOCHDR>\n" + DocUrl + "\n</DOCHDR>\n"  
    return res


def TransferPage(PageStr):
    DocUrl,DocNo = ExtractMetaInfor(PageStr)
    return MakeTrecWebHead(DocUrl,DocNo) + PageStr + '</DOC>'


if 3 != len(sys.argv):
    print '2 para: wiki dump + out name'
    sys.exit()
    
bAfterHead = False
PageStr = ""
out = open(sys.argv[2],'w')

for line in open(sys.argv[1]):
    line = line.strip()
    if not bAfterHead:
        if "<page>" in line:
            bAfterHead = True
        else:
            continue
    PageStr += line + "\n"
    if "</page>" in line:
        print >> out, TransferPage(PageStr)
        PageStr = ""

out.close();  




