from system import *
import sys

args = sys.argv[1:]
f_name = args[0]

s = System(3,3,3)
s.load(f_name)
s.full_dump(f_name)

