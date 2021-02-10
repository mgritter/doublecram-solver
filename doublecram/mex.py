
def nim_addition( *values ):
    a = values[0]
    for b in values[1:]:
        a ^= b
    return a
            
def mex( nimbers ):
    x = set( nimbers )
    for n in range( 0, len( nimbers ) + 1 ):
        if n not in x:
            return n
        
    assert False
    
