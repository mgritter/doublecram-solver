import svgwrite
import math

def drawAt( dwg, shape, x = 0, y = 0, size=10, stroke = "black", fill="gray" ):
    for (xi,yi) in shape.coords:
        dwg.add(dwg.rect((x + xi * size,y + yi * size),
                         (size,size),stroke=stroke,fill=fill))

def isqrt( n ):
    y = int(math.sqrt(n))
    if y * y < n:
        return y+1
    else:
        return y
        
def draw( collection ):
    size = len( collection )
    edge_length = isqrt( size )
        
    grid_size = 10
    max_height = max( s.height() for s in collection )
    max_width = max( s.width() for s in collection )
    x_spacing = (max_width + 2) * grid_size
    y_spacing = (max_height + 2) * grid_size

    d = svgwrite.Drawing( size=(edge_length * x_spacing,
                                edge_length * y_spacing) )
    for (i, s) in enumerate( collection ):
        yi = i // edge_length 
        xi = i % edge_length
        drawAt( d, s, grid_size + xi * x_spacing, grid_size + yi * y_spacing )

    return d

import grid.shape

def test():
    collection = list( grid.shape.enumerate( 4 ) )
    dwg = draw( collection )
    dwg.saveas( "test.svg" )

if __name__ == "__main__":
    test()

