#*-*-coding=utf-8--*-
'''
Created on 2014年7月1日

@author: luobin
'''
import random

class HybridFrame(object):
    '''
    classdocs
    '''
    comelist = [] #elements of job includes a tuple contain (id,cpu,mem,starttime,lifetime) 
    leavelist = [] #elements includes a tuple contain (id,cpu,mem,starttime,lifetime, dealid) 
    deallist = []   #includes a list of (cpu,mem) usage
    queuelist = [] #include of waited job  from comelist
    maxqueue = 0  #max length for the waited queuelist
    currenttime = 0
    
    output_deal =[] #record every time slot there are how many deals each type
    output_job = [] #record every job comgtime,scheduletime,endtime,dealtype,cpu and mem usage 
    
    def __init__(self, filename):
        '''
        Constructor
        '''
        self.deal = {1:[200,50],2:[75,37],3:[100,100],4:[50,75],5:[75,150]}
        fcin = open(filename,"r")
      
        self.fjob = open("output_job.txt",'w')
        self.fdeal = open("output_deal.txt",'w')
        
        for line in fcin:
            jid,cpu,mem,st,lt = line.split() #example 1 15 15  597386942813 252917418
            self.comelist.append([int(jid),int(cpu),int(mem),int(st),int(lt)])
        fcin.close()
    
    def online_approach(self,job):
        """abstract method"""
        pass
    
    def offline_approach(self):
        """abstract method"""
        pass
    
    def preleave(self,leave_record):
        for index in range(len(self.leavelist)):  #time nearest goes first
            if leave_record[5] < self.leavelist[index][5]:
                self.leavelist.insert(index,leave_record)
                return
        self.leavelist.append(leave_record)   
                    
    def allocate(self):
        job = self.comelist.pop(0)
        deal_id = self.online_approach(job)
        if deal_id != 0:
            jobleavetime = self.currenttime + job[4]
            jobleaverecord = [job[0],deal_id,job[1], job[2], self.currenttime,jobleavetime]
            self.preleave(jobleaverecord) # entering the leaving list
        else:
            self.queuelist.append(job)  #otherwise goes into the waiting queue, latest job append to the last           
            if len(self.queuelist) >= self.maxqueue:
                self.offline_approach()
            
    def recover(self):
        #when the jon finished, the resource must be returned
        leaverecord = self.leavelist.pop(0);
        deal_id = leaverecord[1] -1 #numbered from 1
        self.deallist[deal_id][2] -= leaverecord[2]
        self.deallist[deal_id][3] -= leaverecord[3]
        self.fjob.writelines(str(leaverecord)+'\n')

        if self.deallist[deal_id][2] <= 0.01 and self.deallist[deal_id][3] <= 0.01:
                self.deallist.__delitem__(deal_id)
        
        for job in self.queuelist:
            deal_id = self.online_approach(job)
            if deal_id != 0:
                leavetime = self.currenttime + job[4]
                leave_record = [job[0],deal_id,job[1],job[2],self.currenttime,leavetime]
                self.preleave(leave_record) # entering the leaving list

        
    def operate(self):
        self.currenttime = 0
        while True:
            if len(self.comelist)==0 and len(self.leavelist)==0 and len(self.queuelist)==0:
                break
            elif len(self.comelist)==0:
                self.output_deal(self.currenttime, self.leavelist[0][5])
                self.currenttime = self.leavelist[0][5] 
                self.recover()
            elif len(self.leavelist)==0:
                self.output_deal(self.currenttime, self.comelist[0][3])
                self.currenttime = self.comelist[0][3] 
                self.allocate() 
            elif self.comelist[0][3] < self.leavelist[0][5]:
                self.output_deal(self.currenttime, self.comelist[0][3])
                self.currenttime = self.comelist[0][3] 
                self.allocate()
            elif self.comelist[0][3] > self.leavelist[0][3]:
                self.output_deal(self.currenttime, self.leavelist[0][5])
                self.currenttime = self.leavelist[0][3] 
                self.recover()
            else:
                print self.comelist[0][3],self.leavelist[0][5]
                self.currenttime = self.comelist[0][3]
                self.output_deal(self.currenttime, self.leavelist[0][5])
                self.recover()
                self.allocate()
        self.fdeal.close()
        self.fjob.close()
    
    def output_deal(self,start,end):
        """count the deal resource usage per time"""
        cpumemdict = {1:[0,0,0],2:[0,0,0],3:[0,0,0],4:[0,0,0],5:[0,0,0]} #sum,used_cpu,used_mem 
        for d in self.deallist:
            cpumemdict[d[0]][0] += 1
            cpumemdict[d[0]][1] += d[2]
            cpumemdict[d[0]][2] += d[3]
        self.fdeal.writelines(str(start)+' '+str(end)+' '+str(cpumemdict)+'\n')

        
class FirstFit(HybridFrame):
    def __init__(self,filename):
        HybridFrame.__init__(self,filename)
        self.maxqueue = 1
   
    def online_approach(self,job):
        i = 0        
        for d in self.deallist:
            i += 1
            if d[2] + job[1] <= self.deal[d[0]][0] and d[3] + job[2] <= self.deal[d[0]][1]:
                d[2] += job[1]
                d[3] += job[2]
                return i
        return 0   #deal id distributed from number 1,2,3....
    
    def offline_approach(self):
        tempdeallist = []
        while len(self.queuelist) !=0:
            job = self.queuelist.pop()
            tag = False
            num = 0
            for d in tempdeallist:
                num += 1
                if d[2]+job[1] <= self.deal[d[0]][0] and d[3] + job[2] <= self.deal[d[0]][1]: 
                    d[2] += job[1]  #cpu
                    d[3] += job[2]  #mem
                    deal_id = len(self.deallist) + num
                    jobleavetime = self.currenttime+job[4]
                    leave_record = [job[0],deal_id,job[1],job[2],self.currenttime,jobleavetime]
                    self.preleave(leave_record) # entering the leaving list
                    tag = True
                    break
            if tag == False:
                self.queuelist.append(job)
                __type = random.randint(1,5)
                tempdeallist.append([__type,self.currenttime, 0, 0]) #initialized to be 0 used
        for temp in tempdeallist:
            self.deallist.append(temp)
        return
        
class BestMatch(HybridFrame):
    def __init__(self,filename):
        HybridFrame.__init__(self,filename)
        print "best match"
        
class Hybrid(HybridFrame):
    def __init__(self,filename):
        HybridFrame.__init__(self,filename)
        print "hybrid"
        
class Factory(object):
    def craeteApproach(self, approach,filename):
        if approach == "firstfit":
            return FirstFit(filename)
        elif approach == "bestmatch":
            return BestMatch(filename)
        elif approach == "hybrid":
            return Hybrid(filename)
        

if __name__=="__main__":
    filename = "/home/luobin/python/GroupBuying/src/newjob_list3.txt"
    
    factory = Factory()
    test = factory.craeteApproach("firstfit",filename)
    test.operate()
    
    