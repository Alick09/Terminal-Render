import curses 

screen = curses.initscr() 
#curses.noecho() 
curses.curs_set(0) 
screen.keypad(1) 
curses.mousemask(curses.ALL_MOUSE_EVENTS)

screen.addstr("This is a Sample Curses Script\n\n") 

key=0
while key!=27: # Esc to close
    key = screen.getch() 
    #screen.erase()
    if key == curses.KEY_MOUSE:
        _, mx, my, _, _ = curses.getmouse()
        y, x = screen.getyx()
        screen.addstr('mx, my = %i,%i                \r'%(mx,my))
    screen.refresh()

curses.endwin()