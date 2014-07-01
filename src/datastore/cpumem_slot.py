'''
@note: This is a primitive script to test whether the cpu or mem time slot distances
are too large. In fact, we want to result of large amout of jobs are being computing
at the same time.
@author: Robin
@return: a tuple contains three elements (time,cpu,mem), with the demand constraint 
of both cpu and mem are less than 1. Simultaneously, it generates a "newjob_list" as the
benchmark for the later experiment. 
'''
import os
import re

def timelist():
    reslist = []
    newid = 0
    fcin = open('job_list.dat','r')
    fcout = open('newjob_list2.txt','wb')
    
    for line in fcin:
        id,cpu,mem,disk,starttime,scheduletime,finishtime = line.split()
        if float(cpu) <= 0.1 and float(mem) <= 0.1 and float(cpu) > 0 and int(starttime)>0:
            newid += 1
            cpu = int(float(cpu)*1000)
            mem = int(float(mem)*1000)
            fcout.writelines(str(newid)+' '+ str(cpu)+' '+str(mem) + ' '+ \
                             ' '+ starttime + ' '+ str(int(finishtime)-int(scheduletime))+"\n")
            reslist.append((starttime, cpu, mem, 1))
            reslist.append((int(starttime) + int(finishtime) - int(scheduletime), cpu, mem, -1))
    reslist.sort(key = lambda x:int(x[0]))
    print newid
    print len(reslist)
    
    fcout.close()
    fcin.close()
    return reslist
       
if __name__ == "__main__":
    result = timelist()
    print len(result)
    cpu = 0
    mem = 0
    fout = open("cpumem_filter2.dat","wb")
    for line in result:
        cpu += float(line[1]) * line[3]
        mem += float(line[2]) * line[3]
        #print line
        fout.writelines(str(line[0]) + " " + str(cpu) + " " + str(mem)+'\n')

