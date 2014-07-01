from GroupBuy import *

a = FirstFit()
b = BestMatch()


#a = OnlineFF()

#b = OnlineBM("111")

#import commands
#print commands.getoutput('ls /home/luobin/')

# issuelist = [] #variable according to approach
# #deal = dict()
# deal = {'1':800,'2':1000,'3':1200}
# 
# def issuelist():
#     issuelist = []
#     newid = 0
#     fcin = open('newjob_list.dat','r')
#     fcout = open('newjob_list','w')
#     for line in file:
#         
#         id,cpu,mem,disk,starttime,scheduletime,finishtime = line.split()
#         if float(cpu) <= 1 and float(mem) <= 1:
#             newid += 1
#             fcout.writelines(newid,cpu,mem,disk,starttime,int(finishtime) - int(scheduletime))
#             issuelist.append((starttime, newid, cpu, mem, 1))
#             issuelist.append((int(starttime) + int(finishtime) - int(scheduletime),newid, cpu, mem, -1))
#     issuelist.sort(key = lambda x:int(x[0]))
#     fcin.close()
#     print len(issuelist)
#     return issuelist
