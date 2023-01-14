from Utilities import *
from Histogram import Histogram

class Sudoku:
    
    def __init__(self,board):
        self.board = board
        ''' Check if the dimensions are right '''
        width = len(board)
        for i in board:
            assert width == len(i)
        counter = 0
        while width:
            assert width>0
            counter += 1
            width   -= 2*counter-1
        self.Dim = counter
        
        ''' Solution Generator '''
        self.sol_gen = self.find_solution()
        

    def get_square(self,i,j):
        ''' Returns an array with the elements of the square containing cell [i,j] '''
        square = []
        row_range = [ i-i%self.Dim + k for k in range(self.Dim) ]
        col_range = [ j-j%self.Dim + k for k in range(self.Dim) ]
        for r in row_range:
            for c in col_range:
                square.append(self.board[r][c])
        return square

    def isDone(self):
        ''' Checks if there are no empty cells in the sudoku '''
        done = True
        for row in self.board:
            if not done:
                break
            for number in row:
                if number == 0:
                    done = False
                    break
        return done    

    def get_conditional_first(self,condition):
        ''' Gets the smallest coordinates of a cell whose entry satifies a condition '''
        for i,row in enumerate(self.board):
            for j,number in enumerate(row):
                if condition(number):
                    return [i,j]

    def find_solution(self):
        ''' 
            Finds the solution to a Sudoku by brute force 
            Recursive solution generator
        
            Warning: This solver does not check if the initial condition is consistent,
                     it only builds consistently from it
        '''
    
        ''' Exit condition, only checks if there are non-empty cells '''
        if self.isDone():
            yield self.board
            return
    
        ''' Fetch the (lexicographically) smallest empty cell '''
        [i,j] = self.get_conditional_first(lambda x : (x == 0))
    
        ''' Find the missing numbers within its row, column and square '''
        missing_row = find_missing( self.board[i] ,[ k for k in range(1,1+self.Dim*self.Dim) ])
        missing_col = find_missing([ self.board[k][j] for k in range(self.Dim*self.Dim)],[ k for k in range(1,1+self.Dim*self.Dim) ])
        square = self.get_square(i,j)
        missing_sqr = find_missing( square , [ k for k in range(1,1+self.Dim*self.Dim) ] )
    
        ''' 
            Find the missing in common to row, column and square
            These are the options to try 
        '''
        options = []
        missing = []
        find_common(missing_row,missing_col,missing)
        find_common(missing_sqr,missing,options)
    
        ''' Recursively try all posibilities '''
        for opt in options:
            self.board[i][j] = opt
            yield from self.find_solution()
            self.board[i][j] = 0
        return
    
    def collect_solutions(self):
        ''' Aggragates into histograms of the entries all the possible solutions of a sudoku '''
        bins = [i for i in range(1,1+self.Dim*self.Dim)]
        self.histograms = [ [  Histogram(bins) for j in range(self.Dim*self.Dim) ] for i in range(self.Dim*self.Dim) ]
        for sol in self.sol_gen:
            for i,row in enumerate(sol):
                for j,num in enumerate(row):
                    self.histograms[i][j].add(sol[i][j])
    
    
    def __str__(self):
        ''' Pretty print for the Sudoku '''
        hline = (self.Dim*(3*self.Dim+1)+1)*"-"
        rval  = ""
        for i,row in enumerate(self.board):
            rval += ( hline+"\n" if i%self.Dim==0 else "")
            for j,number in enumerate(row):
                rval += ("| " if j%self.Dim==0 else " ")+str(number)+" "
            rval += "|\n"
        rval += hline
        return rval