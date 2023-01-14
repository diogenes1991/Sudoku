from threading import Thread
import time

class JobPool:
    
    ''' Time between checks if any thread is done 
        Here I would like to move to a way od doing this
        (checking to see if any new threads can be created)
        without having this dumb loop. Ideally I would do this via 
        the callback function.
        
    '''
    
    Refresh = 5
    
    def __init__(self,function,jobs_params,nThread=8):
        self.nthr = nThread
        self.func = function
        self.jobp = jobs_params
        self.head = 0
        self.njob = len(jobs_params)
        self.done = 0
        self.actv = 0
        self.rval = [ 0 for i in range(self.njob) ]
    
    def start_next(self):
        
        def worker(threadID):
            print("Starting Thread #"+str(threadID))
            t = time.time()
            self.rval[threadID] = self.func(self.jobp[threadID])
            print("Thread #"+str(threadID),"done, it took (",str(time.time()-t),"secs )")
            self.done += 1
            self.actv -= 1
        
        ''' Break condition '''
        if self.head == len(self.jobp):
            return False
        
        ''' Launch worker '''
        t = Thread(target=worker,args=[self.head])
        self.head += 1
        self.actv += 1
        t.start()
        return True
    
    def run(self):
        while self.done < self.njob:
            while self.actv < self.nthr:
                print("Job #"+str(self.head),"of",self.njob,"(",self.done,")")
                if not self.start_next():
                    break
            time.sleep(self.Refresh)