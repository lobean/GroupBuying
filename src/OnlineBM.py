#*-*-coding=utf-8--*-
'''
Created on 2014骞�鏈�鏃�
@author: luobin
'''

from GroupBuy import HybridFrame

class OnlineBM(HybridFrame):
    '''
    classdocs
    '''
    def __init__(self,filename):
        HybridFrame.__init__(self,filename)
        self.maxqueue = 30
        #self.num = 0
   
    def online_approach(self,job):
        #print "online approach ..."
        i = 0
        available_deal = []      
        for d in self.deallist:
            if d[2] + job[1] <= self.deal[d[0]][0] and d[3] + job[2] <= self.deal[d[0]][1]:
                rate = float((self.deal[d[0]][0] - d[2]))/(self.deal[d[0]][1] - d[3])
                available_deal.append([i,rate])
            i += 1
        
        if len(available_deal) == 0:
            return 0 
        
        available_deal.sort(key = lambda x:x[1])
        job_rate = float(job[1])/job[2]
        for j in range(0,len(available_deal)):
            if job_rate <= available_deal[j][1] or j+1 == len(available_deal):
                dkey = available_deal[j][0]
                self.deallist[dkey][2] += job[1]
                self.deallist[dkey][3] += job[2]
                return self.deallist[dkey][4]

    