from grid import Shape
from grid.shape import plot_text
from doublecram.doublecram import validMoves, makeMove
from doublecram.mex import mex, nim_addition

def solve_position( shape, shape_values ):
    key = shape.key()
    if key in shape_values:
        return shape_values[key]

    vm = validMoves(shape.coords)
    if len( vm ) == 0:        
        shape_values[key] = 0
        return 0

    # Find the nim-values of each successor position
    successorValues = set()
    for move in vm:
        partition = makeMove( shape, move )
        if len( partition ) == 0:
            # print( move, [], "=", 0 )
            successorValues.add( 0 )
            continue

        sub_positions = [ solve_position( s, shape_values )
                          for s in partition ]
        total = nim_addition( *sub_positions )
        #print( move, sub_positions, "=", total )
        successorValues.add( total )

    value = mex( successorValues )
    plot_text( [shape] )
    print( "has nim-value", value )
    shape_values[key] = value
    return value

def solve_square(n, values=None):
    coords = [(x,y) for x in range(n) for y in range(n)]
    start = Shape( coords ).canonical()
    if values is None:
        values = {}
    val = solve_position( start, values )
    return start, val, values
    
if __name__ == "__main__":
    solve_square( 4 )
