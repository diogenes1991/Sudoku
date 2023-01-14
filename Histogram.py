class Histogram:
    def __init__(self,bins):
        self.numpoints = 0
        self.data    = {}
        self.bins    = bins
        for b in self.bins:
            self.data[b] = 0
        
    def add(self,key):
        self.numpoints += 1
        self.data[key] += 1
        
    def __str__(self):
        return str(self.data)