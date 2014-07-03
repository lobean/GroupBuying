

issuelist = []

newid = 0
fcin = open('newjob_list3.txt','r')
fcout = open('newjob_list4.txt','w')

for line in fcin:
    id,cpu,mem,starttime,lifetime = line.split()
    issuelist.append([cpu, mem,starttime, lifetime])
issuelist.sort(key = lambda x:int(x[2]))
fcin.close()

newid=0
for line in issuelist:
    newid += 1
    fcout.writelines(str(newid)+" "+line[0]+" "+line[1]+" "+line[2]+" "+line[3]+'\n')
fcout.close()
    
    