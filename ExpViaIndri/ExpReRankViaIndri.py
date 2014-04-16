'''
Created on Apr 16, 2014
make exp query
call indri api
out evares
@author: cx
'''




import site
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from GenerateExpQueryFile import *
from IndriRelate.IndriRanker import *
from cxBase.base import *

class ExpReRankViaIndriC(cxBaseC):
    
    def Init(self):
        self.NumOfExpTerm = 20
        self.IndriRanker = IndriRankerC()
        self.ExpTermIn = ""
        
    def SetConf(self,ConfIn):
        self.IndriRanker.SetConf(ConfIn)
        conf = cxConf(ConfIn)
        self.NumOfExpTerm = int(conf.GetConf('numofexpterm',self.NumOfExpTerm))
        self.ExpTermIn = conf.GetConf('exptermin')
        return True

    @staticmethod
    def ShowConf():
        print"numofexpterm\nexptermin"
        IndriRankerC.ShowConf()
    
    def Process(self):
        llExpTerm = ReadQExpTerms(self.ExpTermIn)
        MakeExpQFile(llExpTerm,self.ExpTermIn + "_indriq",self.NumOfExpTerm)
        self.IndriRanker.InQuery = self.ExpTermIn + "_indriq"
        self.IndriRanker.Process()
        return True
    
    



    
