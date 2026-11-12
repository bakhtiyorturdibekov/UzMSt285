import sys; sys.path.insert(0,'/home/claude/nb2')
import matplotlib; matplotlib.use('Agg')
from builder import build
from cells_qb import C
build(C,'/home/claude/nb2/qosh_boglash_tezlik.ipynb','/tmp/nbD')
