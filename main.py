from experiment import Experiment

from datafiles.synthetic import SyntheticDatafile
from calculate import Calculate
import os
os.environ.setdefault('ESCDELAY', '25')
import log

def main(stdscr):
    from gui.gui import Gui
    log.init()
    Gui(stdscr)

if __name__ == '__main__':
    from curses import wrapper
    wrapper(main)
