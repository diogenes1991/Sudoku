import matplotlib.pyplot as plt
from Sudoku import Sudoku
from JobPool import JobPool

class PSComputator:
    
    NThreads = 4
    
    def __init__(self,sudoku,nthreads):
        self.sudoku = sudoku
        self.NThreads = nthreads
        self.Dim    = self.sudoku.Dim
        self.histograms = []
        
    def show(self):
        for i,row in enumerate(self.histograms):
            for j,his in enumerate(row):
                print("[",i,",",j,"] =",his)
    
    def show_histograms(self):
        ''' Shows all the histograms using plt '''
        if len(self.histograms)==0:
            print("The Phase Space Histograms have not been generated")
            return
        
        def convert_dict_to_hist(d,axis,offset=0,width=1):
            real_axis = [ a+offset for a in axis ]
            real_weig = [ d[a] if a in d.keys() else 0 for a in axis ]
            h = plt.hist(real_axis,weights=real_weig,rwidth=width)
            plt.show()
            plt.clf()
            
        
        for i,row in enumerate(self.histograms):
            for j,his in enumerate(row):
                print("[",i,",",j,"] :")
                convert_dict_to_hist(his.data,[ i for i in range(1,1+self.Dim*self.Dim) ])
                
    def compute_phase_space(self):
        ''' Computes the space of possible solutions if each clue is removed '''
        self.phase_space = []
        
        ''' Prepare all the data '''
        self.sudoku_data = []
        for i,row in enumerate(self.sudoku.board):
            for j,num in enumerate(row):
                if num != 0:
                    board = [ [ self.sudoku.board[k][l] for l in range(self.Dim*self.Dim) ] for k in range(self.Dim*self.Dim) ]
                    board[i][j] = 0
                    self.sudoku_data.append(board)
        
        '''' Auxiliary function to collect the solutions '''
        def collect_solutions(board):
            sudoku = Sudoku(board)
            sudoku.collect_solutions()
            return sudoku.histograms
        
        ''' Run all the jobs  ''' 
        self.job_pool = JobPool(collect_solutions,self.sudoku_data,self.NThreads)
        self.job_pool.run()
        self.histograms = self.job_pool.rval
        