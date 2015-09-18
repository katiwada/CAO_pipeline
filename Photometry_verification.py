from subprocess import check_call
import os

cwd = input()
os.chdir(cwd)
filename = input()
check_call("sex " + filename, shell=True)










