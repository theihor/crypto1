from system import *
import sys

args = sys.argv[1:]

m = int(args[0])
k = int(args[1])
e = int(args[2])
mp_mode = args[3]
kp_mode = args[4]
output_file = args[5]

s = System(m, k, e, mp_mode = mp_mode, kp_mode = kp_mode)
s.recompute()
s.full_dump(output_file)

