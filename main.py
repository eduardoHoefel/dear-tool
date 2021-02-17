import log
from gui.gui import Gui

from datafiles.syntetic import SynteticDatafile
import os
os.environ.setdefault('ESCDELAY', '25')

def main(stdscr):
    log.init()
    Gui(stdscr)


if __name__ == '__main__':
    from curses import wrapper
    wrapper(main)
