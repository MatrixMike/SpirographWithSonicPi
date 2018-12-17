#spiroRun.py by Robin Newman, December 2018
#version 2 adding support for randcol argument
from Spirograph import Spirograph
import argparse
import time
parser = argparse.ArgumentParser()
parser.add_argument("-r")
parser.add_argument("-sr")
parser.add_argument("-d")
parser.add_argument("-col")
parser.add_argument("-rand")
args=parser.parse_args()
r=int(args.r)
sr=int(args.sr)
d=int(args.d)
col=args.col
randcol=args.rand

s = Spirograph(r)
s.setSmallCircle(sr)
s.setPen(d, col)

s.draw(randcol)

time.sleep(2)
