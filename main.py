"""
*	Mathematical Programming - SME0110
*	Linear Programming - Project 1
*	Travelling Salesman Problem
*
*	@author Matheus Aparecido do Carmo Alves
*	@#usp	9791114
"""
from tsp import *

# 1. Loading the TSP Burma14 dataset
datafile = open('burma14.txt')

# 2. Pre-processing the data
data = []
for line in datafile:
	data.append([float(line[0]),float(line[1])])
datafile.close()

# 2. Solving the TSP via DFG Model
tsp_problem = TSP(data)

print '|| Dantzig-Fulkerson-Johnson Formulation Approach'
for start in range(len(data)):
	print '-- Minimum Route Cost | Start =',start,'\n'
	tsp_problem.dfg(str(str(start)))
	print '\n-----'

# 3. Solving the TSP via 