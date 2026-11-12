import sys; sys.path.insert(0,'/home/claude/nb2')
import matplotlib; matplotlib.use('Agg')
from builder import build
from cells_tezlik import C
build(C,'/home/claude/nb2/tezlik_tahlili.ipynb','/tmp/nbB')
