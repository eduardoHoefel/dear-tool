import log
from gui.gui import Gui

from datafiles.syntetic import SynteticDatafile

def main(stdscr):
    log.init()
    Gui(stdscr)


if __name__ == '__main__':

    from curses import wrapper
    wrapper(main)
