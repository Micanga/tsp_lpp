from copy import copy
from math import sqrt
import numpy as np
from pulp import *
import time

class TSP:

	def __init__(self,data):
		self.data = data
		self.N = len(self.data)

		# defining the graph nodes
		self.x_label = [str(i) for i in range(self.N)]

		# defining the costs
		self.c = self.get_cost()

	def get_cost(self):
		c = dict(((i,j),\
				sqrt(((self.data[int(i)][0] - self.data[int(j)][0])**2) +\
						((self.data[int(i)][1] - self.data[int(j)][1])**2)))\
		 		for i in self.x_label for j in self.x_label if i != j )
		return c

	def dfg(self,start):
		print '1. Defining the objective'
		# 1. Defining the objective
		# a. problem variables
		problem = LpProblem("tsp_dfg",LpMinimize)
		x = LpVariable.dicts('x', self.c, 0, 1, LpBinary)

		cost = lpSum([self.c[(i,j)]*x[(i,j)] for (i,j) in self.c])
		problem += cost

		# b. subtour vatiables
		u = LpVariable.dicts('u', self.x_label,\
		 0, len(self.x_label)-1, LpInteger)

		print '2. Defining the constraints'
		# 2. Defining the contraints
		# a. bounderies contraints
		for k in self.x_label:
			problem += lpSum([ x[(i,k)] for i in self.x_label if (i,k) in x]) == 1
			problem += lpSum([ x[(k,i)] for i in self.x_label if (k,i) in x]) == 1

		# b. subtours constraints (elimination)
		for i in self.x_label:
			for j in self.x_label:
				if i != j and (i != start and j != start) and (i,j) in x:
					problem += u[i] - u[j] <= (self.N)*(1-x[(i,j)]) - 1	

		print '3. Solving by DFG model'
		# 3. Solving by DFG model
		# a. solving
		start_time = time.time()
		problem.solve()
		print '| Time to solve the problem:',(time.time() - start_time),'seconds'
		print '| The solution is',LpStatus[problem.status],'!'

		# b. formating the output
		x_left = copy(self.x_label)
		st = start

		route=[]
		route.append(x_left.pop( x_left.index(st)))

		while len(x_left) > 0:
			for k in x_left:
				if x[(st,k)].varValue ==1:
					route.append( x_left.pop( x_left.index(k)))
					st=k
					break
					
		route.append(start)

		length = sum([self.c[(route[i-1], route[i])] for i in range(1,len(route))])

		# c. printing the result
		print '| Optimal route:'
		print ' -> '.join(route)

		print '| Route length:', length

		return route	
