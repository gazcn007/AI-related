import math
import random

def f(x):
	y=math.sin(x**2.0/2.0)/(x**0.5)
	return y

print f(23)

def Boltzmann_distribution(e,ei,T):
	return math.exp(-(e-ei)/T);

def Simulated_annealing(x0,x_delta,T):
	x=x0
	x1=x0
	while Boltzmann_distribution(x,x1,T)>0.00001 :
		r=random.uniform(-1.0,1.0)
		x1=x+r*x_delta
		p=random.uniform(0.0,1.0)
		print x,x1,T
		if f(x1)>f(x) or Boltzmann_distribution(x,x1,T)>p :
			x=x1
		end
		T=T*0.8
	end

Simulated_annealing(0,0.01,1)