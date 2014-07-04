

# issuelist = []
# 
# newid = 0
# fcin = open('newjob_list3.txt','r')
# fcout = open('newjob_list4.txt','w')
# 
# for line in fcin:
#     id,cpu,mem,starttime,lifetime = line.split()
#     issuelist.append([cpu, mem,starttime, lifetime])
# issuelist.sort(key = lambda x:int(x[2]))
# fcin.close()
# 
# newid=0
# for line in issuelist:
#     newid += 1
#     fcout.writelines(str(newid)+" "+line[0]+" "+line[1]+" "+line[2]+" "+line[3]+'\n')
# fcout.close()
#     
#     
"""
import subprocess
path="/home/luobin/Download/scipoptsuite-3.0.1/scip-3.0.1/examples/Binpacking/bin/"
cmd=path+"binpacking -b batchfile > testout"
subp = subprocess.Popen(cmd,shell = True,cwd=path)
a=subp.wait()
print a

f=open("/home/luobin/Download/scipoptsuite-3.0.1/scip-3.0.1/examples/Binpacking/bin/1.sol","r")
for l in f:
    print l
print "over..."
"""

"""
queuelist=[]
fcin = open("newjob_list4.txt",'r')

for i in range(30):
    line = fcin.readline()
    jid,cpu,mem,st,lt = line.split() #example 1 15 15  597386942813 252917418
    queuelist.append([int(jid),int(cpu),int(mem),int(st),int(lt)])
fcin.close()

fdabao = open("test.bpa","w")
header = "5 30"+'\n'+"100 100 200"+'\n'+"200 50 250"+'\n'+'75 37 113'+'\n'+"50 75 125"+'\n'+"75 150 225"+'\n'
fdabao.writelines(header)
for job in queuelist:
    fdabao.writelines(str(job[0])+" "+str(job[1])+" "+str(job[2])+'\n')
fdabao.close()
"""

import re
def read_file(path):
    reg = re.compile(r'\d+')
    fqubao=open(path+"test.sol","r")
    fqubao.readline()
    fqubao.readline()
    dic = {'250':1,'113':2,'200':3,'125':4,'255':5}
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

if __name__=="__main__":
    path="/home/luobin/Download/scipoptsuite-3.0.1/scip-3.0.1/examples/Binpacking/bin/"
    print read_file(path)


