import sys

# Print all digits that has common bits
def __main__(max_number):

    # Get how many bits are needet to fit the number
    max_power = max_number.bit_length()

    # Map for tile to render
    tile_map = dict()

    # Fill all numbers in tiles
    for i in range( 1, max_number+1 ):
        for bw in range(0, max_power):
            if i & ( 1<<bw  ):
                tile_map.setdefault(bw, []).append(i)

    # Debug
    for row in tile_map.keys():
        print(tile_map[row])


# init
try:
    __main__( int(sys.argv[1]) )
except:
    print( "Usage:", sys.argv[0], "NUMBER", "\n Example: python", sys.argv[0], "10"  )

