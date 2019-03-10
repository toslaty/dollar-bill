import os
import cmd
import sys
from corre import *
from getData import *


class Interp(cmd.Cmd):

	intro ="Welcome to Testestshell Testestshell"
	prompt = '(Shell)'

	def do_get_corr(self,line):
		x = line.split(' ')
		print(x)
		corr_stocks(x[0],x[1],x[2],x[3])

	#def do_get_beta(self, line):
		#x = line.split(' ')

	def do_get_prices(self, line):
	
		p = line.split(' ')	
		git_prices(p[0],p[1], p[2])

	#def do_get_most_profitable():	

	def do_get_fundamentals(self,line):
		x = line.split(' ')
		z = str(x[2])
		get_special(z)

	def do_print(self,line):
		print('Test')




