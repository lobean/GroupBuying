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
    mp = {}
    dealcount =0
    
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
                #print self.leavelist
                return
        self.leavelist.append(leave_record)   
                    
    def allocate(self):
        job = self.comelist.pop(0)
        deal_id = self.online_approach(job)
        if deal_id != 0:
            jobleavetime = self.currenttime + job[4]
            deal_type = self.deallist[self.mp[deal_id]][0]
            jobleaverecord = [job[0],deal_id,job[1], job[2], self.currenttime,jobleavetime,job[3],deal_type]
            self.preleave(jobleaverecord) # entering the leaving list
        else:
            self.queuelist.append(job)  #otherwise goes into the waiting queue, latest job append to the last           
            if len(self.queuelist) >= self.maxqueue:
                self.offline_approach()
            
    def recover(self):
        #when the jon finished, the resource must be returned  
        
        #print self.mp
        #print self.deallist
        #print self.leavelist
        
        leaverecord = self.leavelist.pop(0);
        #print leaverecord
        #print self.mp
        deal_id = self.mp[leaverecord[1]]  #leaverecord[1] numbered from 1
        self.deallist[deal_id][2] -= leaverecord[2]
        self.deallist[deal_id][3] -= leaverecord[3]
        
        result = str(leaverecord[0])
        for i in range(1,8):
            result += ','+str(leaverecord[i])
        self.fjob.writelines(result+'\n')

        if self.deallist[deal_id][2] <= 0 and self.deallist[deal_id][3] <= 0:
            self.deallist.__delitem__(deal_id)
            self.mp.__delitem__(leaverecord[1])
            for key in self.mp.keys():
                if key > leaverecord[1]:
                    self.mp[key] -= 1

        
        for job in self.queuelist:
            deal_key = self.online_approach(job)
            if deal_key != 0:
                leavetime = self.currenttime + job[4]
                deal_type = self.deallist[self.mp[deal_key]][0]
                leave_record = [job[0],deal_key,job[1],job[2],self.currenttime,leavetime,job[3],deal_type]
                self.preleave(leave_record) # entering the leaving list
                self.queuelist.remove(job)

        
    def operate(self):
        self.currenttime = 0
        while True:
            if len(self.comelist)==0 and len(self.leavelist)==0 and len(self.queuelist)==0:
                break
            elif len(self.comelist)==0:
                self.output_deal(self.currenttime, self.leavelist[0][5])
                self.currenttime = self.leavelist[0][5]
                print self.currenttime 
                self.recover()
            elif len(self.leavelist)==0:
                self.output_deal(self.currenttime, self.comelist[0][3])
                self.currenttime = self.comelist[0][3]
                print self.currenttime 
                self.allocate() 
            elif self.comelist[0][3] < self.leavelist[0][5]:
                self.output_deal(self.currenttime, self.comelist[0][3])
                self.currenttime = self.comelist[0][3] 
                print self.currenttime
                self.allocate()
            elif self.comelist[0][3] > self.leavelist[0][5]:
                self.output_deal(self.currenttime, self.leavelist[0][5])
                self.currenttime = self.leavelist[0][5] 
                print self.currenttime
                self.recover()
            else:
                self.currenttime = self.comelist[0][3]
                print self.currenttime
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
        
        result = ""
        for k in range(1,6):
            result+=','+str(k)+','+str(cpumemdict[k][0])+','+str(cpumemdict[k][1])+','+str(cpumemdict[k][2])
            
        self.fdeal.writelines(str(start)+','+str(end)+result+'\n')

        
class FirstFit(HybridFrame):
    def __init__(self,filename):
        HybridFrame.__init__(self,filename)
        self.maxqueue = 1
   
    def online_approach(self,job):      
        for d in self.deallist:
            if d[2] + job[1] <= self.deal[d[0]][0] and d[3] + job[2] <= self.deal[d[0]][1]:
                d[2] += job[1]
                d[3] += job[2]
                return d[4]
        return 0   #deal id distributed from number 1,2,3....
    
    def offline_approach(self):
        tempdeallist = []
        tempdealcount = self.dealcount
        while(len(self.queuelist) != 0):
            job = self.queuelist.pop()
            tag = False
            num = 0
            for d in tempdeallist:
                num += 1
                if d[2]+job[1] <= self.deal[d[0]][0] and d[3] + job[2] <= self.deal[d[0]][1]: 
                    d[2] += job[1]  #cpu
                    d[3] += job[2]  #mem
                    deal_key = tempdealcount + num
                    jobleavetime = self.currenttime+job[4]
                    #print deal_key
                    #print self.mp
                    deal_type = tempdeallist[self.mp[deal_key]-len(self.deallist)][0]

                    leave_record = [job[0],deal_key,job[1],job[2],self.currenttime,jobleavetime,job[3],deal_type]
                    self.preleave(leave_record) # entering the leaving list
                    tag = True
                    break
              
            if tag == False:
                self.queuelist.append(job)
                __type = random.randint(1,5)
                while(self.deal[__type]<job[1] or self.deal[__type]<job[2]):
                    __type = random.randint(1,5)
                self.dealcount += 1
                tempdeallist.append([__type,self.currenttime, 0, 0, self.dealcount]) #initialized to be 0 used
                self.mp[self.dealcount] = len(self.deallist) + len(tempdeallist) -1
                #print self.mp
        
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
    filename = "/home/luobin/python/GroupBuying/src/newjob_list4.txt"
    
    factory = Factory()
    test = factory.craeteApproach("firstfit",filename)
    test.operate()
    
    