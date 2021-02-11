from grid import Shape
from grid.shape import plot_text

def validMoves( coords ):
    free = set( coords )
    moves = []
    for (x,y) in coords:
        if (x+1,y) in free and (x,y+1) in free and (x+1,y+1) in free:
            moves.append( (x,y) )
    return moves

def trimShape( shape ):
    covered = set()
    for (x,y) in validMoves( shape ):
        covered.add( (x,y) )
        covered.add( (x+1,y) )
        covered.add( (x,y+1) )
        covered.add( (x+1,y+1) )
    return Shape( covered )

def canCover( free, x, y ):
    """Can some valid move cover square x,y?"""
    #
    #  xx.  .xx   ...  ...
    #  Ax.  .xB   Ax.  .xB
    #  ...  ...   xx.  .xx
    
    if (x-1,y) in free:
        if (x,y-1) in free and (x-1,y-1) in free:
            return True
        if (x,y+1) in free and (x-1,y+1) in free:
            return True
    if (x+1,y) in free:
        if (x,y-1) in free and (x+1,y-1) in free:
            return True
        if (x,y+1) in free and (x+1,y+1) in free:
            return True
    return False

def jointCoverOrthogonal( free, x, y, nx, ny ):
    """Can some valid move cover square x,y and nx,ny?
    Can assume they are orthogonal squares and both in free already."""
    #
    #  .1*   *1.   .**   ...
    #  .2*   *2.   .12   .12
    #  ...   ...   ...   .**


    if x == nx:
        if ( x+1, y ) in free and ( x+1, ny ) in free:
            return True        
        if ( x-1, y ) in free and ( x-1, ny ) in free:
            return True
        return False
    elif y == ny:
        if ( x, y+1 ) in free and ( nx, y+1 ) in free:
            return True        
        if ( x, y-1 ) in free and ( nx, y-1 ) in free:
            return True
        return False
    else:
        assert False

def decompose( coords ):
    free = set( coords )
    components = []
    visited = set()
    
    def dfs( x, y ):
        # Only consider each square once
        if (x,y) in visited:
            return
        visited.add( (x,y) )

        # If we cannot cover the square, leave it out
        # of the decomposition.
        if not canCover( free, x, y ):
            return

        # Otherwise add it to the current component
        components[-1].append( (x,y) )

        # And visit its orthogonal neighbors
        for (nx, ny) in [ (x+1,y), (x-1,y), (x,y-1), (x,y+1) ]:
            # Must be a free square
            if not (nx,ny) in free:
                continue

            # Must have a 2x2 square that covers both!
            # otherwise there is no interaction between the regions, i.e.
            #  xx
            #  xx
            #   xx
            #   xx
            if not jointCoverOrthogonal( free, x, y, nx, ny ):
                continue
            
            dfs( nx, ny )

    for (x,y) in free:
        if (x,y) in visited:
            continue
        components.append( [] )
        dfs( x,y )
        if len( components[-1] ) == 0:
            # Did not find any new squares
            components.pop()

    return components

def test():
    coords = [ (0,0), (1,0),
               (0,1), (1,1), (2,1), (3,1),
               (2,2), (3,2) ]

    coords3 = [ (0,0), (1,0),
               (0,1), (1,1),
               (0,2),
               (0,3), (1,3),
               (0,4), (1,4),
               (3,1), (4,1),
               (3,2), (4,2), (5,2),
               (4,3), (5,3) ]
    plot_text( [Shape( coords )] )

    print( "valid moves", validMoves( coords ) )

    partition = decompose( coords )
    print( "partition", partition )
    shapes = [ Shape( p ) for p in partition ]
    plot_text( shapes ) 
              
if __name__ == "__main__":
    test()

def makeMove( shape, coord ):
    squares = set( shape.coords )
    x,y = coord
    squares.remove( (x,y) )
    squares.remove( (x+1,y) )
    squares.remove( (x,y+1) )
    squares.remove( (x+1,y+1) )

    return [ Shape(p).canonical() for p in decompose( squares ) ]

def showMove( shape, coord ):
    squares = set( shape.coords )
    x,y = coord
    squares.remove( (x,y) )
    squares.remove( (x+1,y) )
    squares.remove( (x,y+1) )
    squares.remove( (x+1,y+1) )

    return [ Shape(p) for p in decompose( squares ) ]

    

