#spiroRun.py by Robin Newman, December 2018
from Spirograph import Spirograph
import argparse
import time
parser = argparse.ArgumentParser()
parser.add_argument("-r")
parser.add_argument("-sr")
parser.add_argument("-d")
parser.add_argument("-col")
args=parser.parse_args()
r=int(args.r)
sr=int(args.sr)
d=int(args.d)
col=args.col

s = Spirograph(r)
s.setSmallCircle(sr)
s.setPen(d, col)

s.draw()

time.sleep(2)
