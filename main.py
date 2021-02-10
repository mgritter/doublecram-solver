from doublecram.solve import solve_square
from doublecram.doublecram import validMoves, makeMove
from doublecram.mex import nim_addition
from grid.shape import plot_text

import sys

size = 5

if len(sys.argv) > 1:
    size = int(sys.argv[1] )
    
square, square_val, values = solve_square( size )

print( "square has nim-value", square_val )

if square_val == 0:
    print( "first player loss" )
else:
    vm = validMoves(square.coords)

    for move in vm:
        partition = makeMove(square, move )
        if len( partition ) == 0:
            print( "optimal move is", move )
            break

        sub_positions = [ values[s.key()] for s in partition ]
        total = nim_addition( *sub_positions )
        if total == 0:
            print( "optimal move is", move, "to:" )
            plot_text( partition )
            break
