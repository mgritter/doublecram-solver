
class Shape(object):
    def __init__( self, coords = None ):
        # X,Y coordinates in the shape
        if coords is None:
            self.coords = []
        else:
            self.coords = list( coords )
        
    def shiftToZero( self ):
        """Move the shape so that the leftmost and bottommost coordinates are
        both 0."""
        if len( self.coords ) == 0:
            return
        minX = min( x for (x,y) in self.coords )
        minY = min( y for (x,y) in self.coords )
        self.coords = [ (x-minX, y-minY) for (x,y) in self.coords]
        self.coords.sort()
        assert self.coords[0][0] >= 0
        assert self.coords[0][1] >= 0

    def compare( self, other ):
        """Compare lexicographic order of coordinates, which are
        assumed to be sorted by x and then y,"""

        # This is unnecessary, the default comparison on key()
        # works fine.
        for a,b in zip( self.coords, other.coords ):
            if a < b:
                return -1
            if a > b:
                return 1

        if len( self.coords ) < len( other.coords ):
            return -1
        elif len( self.coords ) > len( other.coords ):
            return 1
        else:
            return 0

    #   \C A/
    #    \ /E
    # ----o----
    #   D/ \  
    #   /  B\ 
    def flipVertical( self ):
        """Return the shape flipped about the vertical axis.""" 
        s = Shape( [ (-x,y) for (x,y) in self.coords] )
        s.shiftToZero()
        return s

    def flipHorizontal( self ):
        """Return the shape flipped about the horizontal axis.""" 
        s = Shape( [ (x,-y) for (x,y) in self.coords] )
        s.shiftToZero()
        return s

    def flipAscendingDiagonal( self ):
        """Return the shape flipped about the line y=x.""" 
        s = Shape( [ (y,x) for (x,y) in self.coords] )
        s.shiftToZero()
        return s
    
    def flipDescendingDiagonal( self ):
        """Return the shape flipped about the line y=-x.""" 
        s = Shape( [ (-y,-x) for (x,y) in self.coords] )
        s.shiftToZero()
        return s

    #      A
    #   D   
    # ----o----
    #       B
    #    C  
    def rotate90( self ):
        """Rotate 90 degrees (counterclockwise) around the origin."""
        s = Shape( [ (-y, x) for (x,y) in self.coords] )
        s.shiftToZero()
        return s

    def rotate180( self ):
        """Rotate 180 degrees around the origin."""
        s = Shape( [ (-x, -y) for (x,y) in self.coords] )
        s.shiftToZero()
        return s

    def rotate270( self ):
        """Rotate 270 degrees around the origin."""
        s = Shape( [ (y, -x) for (x,y) in self.coords] )
        s.shiftToZero()
        return s

    def key( self ):
        return tuple( self.coords )

    def canonical( self ):
        """Return the lexicographically smallest of the shape under
        the symmetries of the square"""
        identity = Shape( self.coords )
        identity.shiftToZero()
        return min( identity,
                    self.rotate90(),
                    self.rotate180(),
                    self.rotate270(),
                    self.flipVertical(),
                    self.flipHorizontal(),
                    self.flipAscendingDiagonal(),
                    self.flipDescendingDiagonal(),
                    key = lambda x : x.key() )
    
    def height( self ):
        return max( y for (x,y) in self.coords ) + 1

    def width( self ):
        return max( x for (x,y) in self.coords ) + 1
    
    def plot( self, w = None, h = None ):
        if h is None:
            h = self.height()
        if w is None:
            w = self.width()
        grid = [ [ " " for x in range(w) ] for y in range( h ) ]
        for (x,y) in self.coords:
            grid[y][x] = "#"
        return "\n".join( "".join( row ) for row in grid )

import itertools

def enumerate( n ):
    result = set()
    all_coords = [ (x,y) for x in range( n ) for y in range( n ) ]
    for pop in range( 1, n * n + 1 ):
        for c in itertools.combinations( all_coords, r=pop ):
            s = Shape( c ).canonical()
            k = s.key()
            if k not in result:
                result.add( k )
                yield s
                
def plot_text( collection, n = 10 ):
    for s in collection:
        print( "-" * n )
        print( s.plot() )

    print( "-" * n )

        
def test():
    # xxx  
    # xxx  
    # xxx  
    #   xxx
    #   xxx
    #
    # vs
    #
    # xxx  
    # xxx  
    # xxxxx
    #    xx
    #    xx
    
    s1 = Shape( [(0,0),(1,0),(2,0),
                 (0,1),(1,1),(2,1),
                 (0,2),(1,2),(2,2),
                 (2,3),(3,3),(4,3),
                 (2,4),(3,4),(4,4)] )
    s1.coords.sort()
    
    s2 = Shape( [(0,0),(1,0),(2,0),
                 (0,1),(1,1),(2,1),
                 (0,2),(1,2),(2,2),(3,2),(4,2),
                 (3,3),(4,3),
                 (3,4),(4,4)] )
    s2.coords.sort()

    all = [ s1, 
            s1.rotate90(),
            s1.rotate180(),
            s1.rotate270(),
            s1.flipVertical(),
            s1.flipHorizontal(),
            s1.flipAscendingDiagonal(),
            s1.flipDescendingDiagonal() ]
    all.sort(  key = lambda s : s.key() )

    print( "s1 sort order:" )
    plot_text( all )
    
    all = [ s2, 
            s2.rotate90(),
            s2.rotate180(),
            s2.rotate270(),
            s2.flipVertical(),
            s2.flipHorizontal(),
            s2.flipAscendingDiagonal(),
            s2.flipDescendingDiagonal() ]
    all.sort( key = lambda s : s.key() )

    print( "s2 sort order:" )
    plot_text( all )
    
    s1c = s1.canonical()
    s2c = s2.canonical()
    if s1c.key() != s2c.key():
        print( "do not match" )
        print( s1c.key() )
        print( s2c.key() )
    plot_text( [s1, s1c, s2, s2c] )
                 

if __name__ == "__main__":
    test()
        
