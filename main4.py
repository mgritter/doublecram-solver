from doublecram.solve import solve_mn
from doublecram.svg import gameTree
from grid import Shape

import sys

height = 4
size = 20

if len(sys.argv) > 1:
    size = int(sys.argv[1] )
    
rect, rect_val, values = solve_mn( height, size )
#d = gameTree( rect, values )
#d.saveas( "game-tree-{}x{}.svg".format( height, size ) )

for i in range(2,size+1):
    coords = [(x,y) for x in range(i) for y in range(height)]
    rect = Shape( coords ).canonical()
    key = rect.key()
    if key in values:
        print( "{:2d}x{:2d} = {}".format( i, height, values[key] ))
