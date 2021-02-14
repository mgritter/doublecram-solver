import svgwrite
from doublecram.doublecram import showMove, validMoves
from doublecram.solve import solve_square

red = {
    "edge_stroke" : "none",
    "odd_square" : "red",
    "even_square" : "red"
    
}

blue = {
    "edge_stroke" : "#2e7597",
    "odd_square" : "#16263d",
    "even_square" : "#2d5f6b"
}

green = {
    "edge_stroke" : "#4a5645",
    "odd_square" : "#588e28",
    "even_square" : "#a8ce53"
}

purple = {
    "edge_stroke" : "#753e42",
    "odd_square" : "#b47560",
    "even_square" : "#ebbd92"
}

def drawRegion( dwg, coords, x = 0, y = 0, size=10, edge_stroke = "black",
                odd_square = "gray", even_square = "lightgray" ):
    g = dwg.g()
    for (xi,yi) in coords:
        corner_x = x + xi * size
        corner_y = y + yi * size
        if (xi + yi) % 2 == 0:
            dwg.add(dwg.rect((corner_x, corner_y),
                             (size,size),stroke="none",fill=even_square))
        else:
            dwg.add(dwg.rect((corner_x, corner_y),
                             (size,size),stroke="none",fill=odd_square))
        if (xi+1,yi) not in coords:
            # right border
            g.add(dwg.line((corner_x + size, corner_y),
                             (corner_x + size, corner_y + size),
                             stroke=edge_stroke,
                             stroke_linecap="square"))
        if (xi-1,yi) not in coords:
            # left border
            g.add(dwg.line((corner_x, corner_y),
                             (corner_x, corner_y + size),
                             stroke=edge_stroke,
                             stroke_linecap="square"))
        if (xi,yi-1) not in coords:
            # top border
            g.add(dwg.line((corner_x, corner_y),
                             (corner_x + size, corner_y),
                             stroke=edge_stroke,
                             stroke_linecap="square"))
        if (xi,yi+1) not in coords:
            # bottom border
            g.add(dwg.line((corner_x, corner_y + size),
                             (corner_x + size, corner_y + size),
                             stroke=edge_stroke,
                             stroke_linecap="square"))

    # Add border last so it is on top.
    dwg.add(g)
            
class Position(object):
    def __init__( self, parent, parentShape, moveCoords, partitions, values ):
        self.parent = [ parent ]
        self.parentShape = parentShape
        self.move = moveCoords
        self.partitions = partitions
        self.values = values
        
def gameTree( shape, values, maxLevels = 4 ):
    max_width = max( x for (x,y) in shape.coords ) + 1
    max_height = max( y for (x,y) in shape.coords ) + 1
    x_spacing = (max_width + 2) * 10
    y_spacing = (max_height + 8) * 10
    min_x = 0
    
    levels = [[shape]]
    for i in range( 1, maxLevels ):
        prevLevel = levels[-1]
        nextLevel = {}
        for j, position in enumerate( prevLevel ):
            if i == 1:
                s = position
            else:
                if len( position.partitions ) != 1:
                    continue
                s = position.partitions[0].canonical()
            
            vm = validMoves(s.coords)
            if len( vm ) == 0:        
                continue

            for (mx,my) in vm:
                # pieces of the partition are not made canonical yet
                partition = showMove( s, (mx,my) )
                canonical = [ x.canonical().key() for x in partition ]
                partition_values = [ values[x] for x in canonical ]

                # Only show each resulting position once
                canonical.sort()
                key = tuple( canonical )
                if key in nextLevel:
                    nextLevel[key].parent.append( j )
                else:
                    move_coords = set( [ (mx, my), (mx+1, my),
                                         (mx,my+1), (mx+1,my+1) ] )
                    nextLevel[key] = Position( j,
                                               s,
                                               move_coords,
                                               partition,
                                               partition_values )
                
        levels.append( list( nextLevel.values() ) )
                
    d = svgwrite.Drawing()
    anchors = {}
    for i, level in enumerate( levels ):
        if i == 0:
            drawRegion( d, level[0].coords, 0, 0 )
            anchors[(0,0)] = (max_width * 5, max_height * 10 + 20 )

            if values[shape.key()] == 0:
                label = 0
            else:
                label = "*" + str( values[shape.key()] )
                
            d.add( d.text( label,
                           insert = ( max_width * 5,
                                      max_height * 10 + 10 ),
                           font_size = "10",
                           font_family = ["Arial", "Helvetica", "sans-serif" ],
                           text_anchor = "middle"))
            
            continue
        numToDraw = len( level )
        x_start = -(numToDraw * x_spacing) / 2
        if x_start < min_x:
            min_x = x_start
        y_start = y_spacing * i
        colors = [blue, green, purple]
        
        for j, p in enumerate( level ):
            remaining = set( p.parentShape.coords )
            remaining.difference_update( p.move )
            for part in p.partitions:
                remaining.difference_update( part.coords )

            anchors[(i,j)] = (x_start + j * x_spacing + max_width * 5,
                              y_start + max_height * 10 + 20 )
                
            drawRegion( d, remaining,
                        x_start + j * x_spacing,
                        y_start,
                        edge_stroke = "none" )
            drawRegion( d, p.move,
                        x_start + j * x_spacing,
                        y_start,
                        **red )
            for k, part in enumerate( p.partitions ):
                drawRegion( d, part.coords,
                            x_start + j * x_spacing,
                            y_start,
                            **(colors[k%len(colors)]) )

            if len( p.partitions ) == 0:
                label = "0"
            else:
                label = " + ".join( "*" + str(v) for v in p.values )
                
            d.add( d.text( label,
                           insert = ( x_start + j * x_spacing + max_width * 5,
                                      y_start + (max_height * 10 + 10) ),
                           font_size = "10",
                           font_family = ["Arial", "Helvetica", "sans-serif" ],
                           text_anchor = "middle"))

            for parent_index in p.parent:
                d.add( d.line( (x_start + j * x_spacing + max_width * 5,
                                y_start - 10),
                               anchors[(i-1,parent_index)],
                               stroke="black" ) )


    d.viewbox( min_x, - x_spacing, -2 * min_x + x_spacing, (len( levels )+1) * y_spacing )
    return d


def colorDemo():
    d = svgwrite.Drawing()
    coords = set(
        [ (0,0), (1,0), (2,0),
          (0,1), (1,1), (2,1),
                 (1,2), (2,2), (3,2),
                 (1,3), (2,3), (3,3) ] )
    drawRegion( d, coords )
    drawRegion( d, coords, x = 60, y = 0, **blue )
    drawRegion( d, coords, x = 0, y = 60, **green )
    drawRegion( d, coords, x = 60, y = 60, **purple )
    
    drawRegion( d, coords, x = 120, y = 0 )
    drawRegion( d, [ (1,0), (2,0), (1,1), (2,1) ], x = 120, y = 0, **red)
    d.saveas( "color-demo.svg" )

def treeDemo():
    square, _, values = solve_square( 5 )
    d = gameTree( square, values )
    d.saveas( "game-tree.svg" )
    
if __name__ == "__main__":
    treeDemo()
    
    
    
