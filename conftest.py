import sys
from os.path import abspath
from os.path import dirname as d
from os.path import join

root_dir = d(abspath(__file__))
sys.path.append(root_dir)
