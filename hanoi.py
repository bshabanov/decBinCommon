import sys
import curses

topline = (" "*4+"||"+" "*4) * 3
bottomline = "=" * 30

disk = [
    "[  ||  ]",
    " [ || ] ",
    "  [||]  "
]

poles = [
    0b111,
    0b000,
    0b000
]

lock = False
carry = 0b000
position = 0
steps = 0
loop = True

def base(window):
        window.addstr(2, 5, "Steps: "+str(steps))
        window.addstr(4, 5, topline)
        window.addstr(5, 5, topline)
        window.addstr(6, 5, topline)
        window.addstr(7, 5, topline)
        window.addstr(8, 5, bottomline)
        window.addstr(9, 9 + position * 10, "XX")


def disks(window):
    if (carry != 0):
        calc = int(carry/2)
        window.addstr(3, 6+position*10, disk[calc])
    for i in range(3):
        height = 0;
        for j in range(3):
            if (poles[i] & 1<<j):
                window.addstr(7-height, 6+i*10, disk[j])
                height+=1



def move(command):
    global lock
    global poles
    global carry
    global steps
    global position
    if (command == 260 and position > 0):
        position-=1
    if (command == 261 and position < 2):
        position+=1
    if (command == 32):
        if (lock):
            if (poles[position]<carry):
                poles[position] |= carry
                carry = 0b000
                steps+=1
        if (not lock):
            for i in range(3):
                j = 2-i
                if (poles[position] & 1<<j):
                    carry = 1<<j
                    poles[position] &= ~(1<<j)
                    lock = True
                    break
        if (carry == 0):
            lock = False


def isSolved(window):
    global loop
    if (poles[2] == 0b111):
        window.addstr(1,5, "You win")
        loop = False


def main(window):
    window.clear()
    window.refresh()
    curses.curs_set(0)
    command = 0
    while loop and command != 113:
        window.clear()
        move(command)
        base(window)
        disks(window)
        isSolved(window)
        command = window.getch()


curses.wrapper(main)
