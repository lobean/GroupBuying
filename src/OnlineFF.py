#OnlineFF.py
#Online First Fit

class OnlineFF(object):
    deallist = []
    def __init__(self):
        print "Hello"
    def firstfit(self,filename):
        f = open(filename,'r')
        
        job = f.readline()
        queue.append(job)
        
    
    
if __name__ == "__main__":
    ff = OnlineFF()
    ff.firstfit()