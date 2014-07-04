from GroupBuy import HybridFrame

import re

class FirstHybrid(HybridFrame):
    def __init__(self,filename):
        HybridFrame.__init__(self,filename)
        self.maxqueue = 30
        self.num = 0
   
    def online_approach(self,job):
        #print "online approach ..."
        i = 0      
        for d in self.deallist:
            if d[2] + job[1] <= self.deal[d[0]][0] and d[3] + job[2] <= self.deal[d[0]][1]:
                self.deallist[i][2] += job[1]
                self.deallist[i][3] += job[2]
                return d[4]
            i += 1
        return 0   #deal id distributed from number 1,2,3....
    
    def offline_approach(self):
        
        path="/home/luobin/Download/scipoptsuite-3.0.1/scip-3.0.1/examples/Binpacking/bin/"
        #print "offline approach ..."
        self.write_file(path)
        self.system_call(path) #call the binpacking shell
        dealjoblist = self.read_file(path)
        
        self.num += 1
        
        jobset = [] #a set of job for no repeated
        for dealjob in dealjoblist:
            deal_type = dealjob[0]
            self.dealcount += 1
            dcpu = 0
            dmem = 0
            for i in range(1,len(dealjob)):
                if dealjob[i] in jobset:
                    continue
                else:
                    jobset.append(dealjob[i])
                    jid = dealjob[i]
                    deal_id = self.dealcount
                    for qjob in self.queuelist:
                        if qjob[0] == jid:
                            jcpu = qjob[1]
                            jmem = qjob[2]
                            submittime = qjob[3]
                            jobleavetime = self.currenttime + qjob[4]
                            leave_record = [jid,deal_id,jcpu,jmem,self.currenttime,jobleavetime,submittime,deal_type]
                            self.preleave(leave_record)
                            dcpu += jcpu
                            dmem += jmem
                            break
            self.deallist.append([deal_type,self.currenttime, dcpu, dmem, self.dealcount]) #add new deal               
            self.mp[self.dealcount] = len(self.deallist) -1
        while len(self.queuelist) != 0:
            self.queuelist.pop()
        return
    
    def write_file(self,path):
        """Unit test passed"""
        fdabao = open(path+str(self.num)+"test.bpa","w")
        header = "dabao"+'\n'+"5 30"+'\n'+"100 100 200"+'\n'+"200 50 250"+'\n'+'75 37 113'+'\n'+"50 75 125"+'\n'+"75 150 225"+'\n'
        fdabao.writelines(header)
        for job in self.queuelist:
            fdabao.writelines(str(job[0])+" "+str(job[1])+" "+str(job[2])+'\n')
        fdabao.close()
        fbatch = open(path+str(self.num)+"batchfile","w")
        batstr = "set limits gap 0.05"+'\n'+"read "+str(self.num)+"test.bpa"+'\n'+"optimize"+'\n'+"write solution "+str(self.num)+"test.sol"+'\n'+"free"+'\n'+"quit"
        fbatch.writelines(batstr)
        
    def read_file(self,path):
        reg = re.compile(r'\d+')
        fqubao=open(path+str(self.num)+"test.sol","r")
        fqubao.readline()
        fqubao.readline()
        dic = {'250':1,'113':2,'200':3,'125':4,'225':5}
        dealjoblist = []
        index = -1
        while True:
            jlist = []
            line = fqubao.readline()
            if not line:
                break
            else:
                index += 1
                item = reg.findall(line)
                if len(item) == 0:
                    print "length error"
                
                for i in range(len(item)-2):
                    jid = int(item[i])
                    jlist.append(jid)
                dealjoblist.append(jlist)
                dealjoblist[index].insert(0,dic[item[len(item)-1]])
        fqubao.close()
        return dealjoblist
        
    
    def system_call(self,path):
        """Unit test passed"""
        import subprocess
        cmd=path+"binpacking -b "+str(self.num)+"batchfile > testout"
        subp = subprocess.Popen(cmd,shell = True,cwd=path)
        subp.wait()
        #print "system call ..."
        
if __name__=="__main__":
    filename = "testjob_list.txt"
    fh = FirstHybrid(filename)
    fh.operate()
    print "over"
