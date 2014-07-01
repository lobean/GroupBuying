#*-*-coding=utf-8--*-
'''
Created on 2014年7月1日

@author: luobin
'''

class HybridFrame(object):
    '''
    classdocs
    '''
    comelist = [] #elements of job includes a tuple contain (id,cpu,mem,starttime,lifetime) 
    leavelist = [] #elements includes a tuple contain (id,cpu,mem,starttime,lifetime, dealid) 
    deallist = []   #includes a list of (cpu,mem) usage
    queuelist = [] #include of waited job  from comelist
    maxqueue = 0  #max length for the waited queuelist
    
    def __init__(self, filename):
        '''
        Constructor
        '''
        self.deal = {'1':800,'2':1000,'3':1200}
        fcin = open(filename,"r")
        for line in fcin:
            print line.split()
            self.comelist.append(line.split())
        fcin.close()
    
    def approach(self,job):
        """abstract method"""
        pass
    
    def enterwaiting(self,job,tag):
        """abstract method"""
        pass
    
    def allocate(self):
        job = self.comelist.pop(0)
        
        tag = self.approach(job)
        if tag != 0:
            self.enterwaiting(job, tag)
   
    def recover(self):
        #when the jon finished, the resource must be returned
        issue = self.leavelist.pop(0);
        self.deallist[int(issue[5])][0] += issue[3]
        self.deallist[int(issue[5])][1] += issue[4]
    
    def operate(self):
        if self.comelist[0][3] < self.leavelist[0][3]:
            self.allocate()
        else:
            self.recover()
    
    def output(self):
        """output the resource usage per time"""
        pass
        
class FirstFit(HybridFrame):
    def __init__(self,filename):
        HybridFrame.__init__(self,filename)
        self.maxqueue = 1
   
    def approach(self):
        pass
    
    def enterwaiting(self,job,tag):
        pass
        
class BestMatch(HybridFrame):
    def __init__(self,filename):
        HybridFrame.__init__(self,filename)
        print "best match"
        
class Hybrid(HybridFrame):
    def __init__(self,filename):
        HybridFrame.__init__(self,filename)
        print "hybrid"
        
class Factory:
    def craeteApproach(self, approach,filename):
        if approach == "firstfit":
            return FirstFit(filename)
        elif approach == "bestmatch":
            return BestMatch(filename)
        elif approach == "hybrid":
            return Hybrid(filename)
        

if __name__=="__main__":
    filename = "newjob_list.txt"
    
    factory = Factory()
    test = factory.craeteApproach("firstfit",filename)
    test.operate()
    
    