import sys
import curses

def run(window, number, power):
    window.clear()
    window.refresh()

    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Map for tile to render
    tile_map = dict()

    # Fill all numbers in tiles
    for i in range( 1, number+1 ):
        for bw in range(0, power):
            if i & ( 1<<bw  ):
                tile_map.setdefault(bw, []).append(i)


    command = 0
    score = 0

    for row in tile_map.keys():
        reshaped = dict();
        for index in range(len(tile_map[row])):
            reshaped.setdefault(int(index/10),  []).append(tile_map[row][index])

        window.clear()
        window.addstr( 2, 5, "Do you see your number?", curses.color_pair(1))
        for index in reshaped.keys():
            window.addstr(4+index, 5, ", ".join(format(e, str(len(str(number)))) for e in reshaped[index]), curses.color_pair(1))

        listLen = len(reshaped.keys())
        mod = 5
        picked = False
        scoreMod = 0

        window.addstr(listLen+mod, 4, "  Yes ", curses.color_pair(1))
        window.addstr(listLen+mod, 10, "  No ", curses.color_pair(1))

        while command != 10 or picked == False:
            if command == curses.KEY_LEFT:
                window.addstr(listLen+mod, 4, " ►Yes ", curses.color_pair(2))
                window.addstr(listLen+mod, 10, "  No ", curses.color_pair(1))
                picked = True
                scoreMode = 2**row
               
            if command == curses.KEY_RIGHT:
                window.addstr(listLen+mod, 4, "  Yes ", curses.color_pair(1))
                window.addstr(listLen+mod, 10, " ►No ", curses.color_pair(2))
                picked = True
                scoreMode = 0

            command = window.getch()
        command = 0
        picked = False
        score += scoreMode
        scoreMode = 0

    # Show number
    boxtemplate = "" * (21 + len(str(score)))
    window.clear()
    window.addstr( 4, 5, boxtemplate, curses.color_pair(2))
    window.addstr( 5, 5, "  Your number is: " + str(score)+"  ", curses.color_pair(2))
    window.addstr( 6, 5, boxtemplate, curses.color_pair(2))

    window.getch()


def __main__(n):
    # Render screen
    curses.wrapper(run, n, n.bit_length())


# init
try:
    __main__( int(sys.argv[1]) )
except curses.error as error:
    print( "Screen is too small to print numbers. Try with smaller NUMBER" )
except Exception as inst:
    print( "Usage:", sys.argv[0], "NUMBER", "\nPython will guess the number between 1 and NUMBER", "\nExample: python", sys.argv[0], "10" )

