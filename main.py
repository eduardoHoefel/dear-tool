import log
from gui.gui import Gui

from datafiles.synthetic import SyntheticDatafile
import os
os.environ.setdefault('ESCDELAY', '25')

def main(stdscr):
    log.init()
    Gui(stdscr)


if __name__ == '__main__':
    from curses import wrapper
    wrapper(main)
