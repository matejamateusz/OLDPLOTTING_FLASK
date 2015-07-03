#!/usr/bin/python

#from subprocess import Popen, PIPE
#eval(Popen(['python', 'ExpCondAnalyser.py', '-r', '133698', '-T', '-bla'], stdout=PIPE).communicate()[0])
from subprocess import call 
call(['python', 'ExpCondAnalyser.py', '-r', '133698', '-T', '-bla'])


