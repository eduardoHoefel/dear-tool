import abc
import math
import shutil
import sys

from typing import TextIO

"""
Code found on Mike's blog
https://mike42.me/blog/2018-06-make-better-cli-progress-bars-with-unicode-block-characters
"""

"""
Produce progress bar with ANSI code output.
"""
class ProgressBar(object):
    def __init__(self, target: TextIO = sys.stdout):
        self._target = target
        self._text_only = not self._target.isatty()
        self._update_width()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if(exc_type is None):
            # Set to 100% for neatness, if no exception is thrown
            self.update(1.0)
        if not self._text_only:
            # ANSI-output should be rounded off with a newline
            self._target.write('\n')
        self._target.flush()
        pass

    def _update_width(self):
        self._width, _ = shutil.get_terminal_size((80, 20))

    def update(self, progress : float):
        # Update width in case of resize
        self._update_width()
        # Progress bar itself
        if self._width < 12:
            # No label in excessively small terminal
            percent_str = ''
            progress_bar_str = ProgressBar.progress_bar_str(progress, self._width - 2)
        elif self._width < 40:
            # No padding at smaller size
            percent_str = "{:6.2f} %".format(progress * 100)
            progress_bar_str = ProgressBar.progress_bar_str(progress, self._width - 11) + ' '
        else:
            # Standard progress bar with padding and label
            percent_str = "{:6.2f} %".format(progress * 100) + "  "
            progress_bar_str = " " * 5 + ProgressBar.progress_bar_str(progress, self._width - 21)
        # Write output
        if self._text_only:
            self._target.write(progress_bar_str + percent_str + '\n')
            self._target.flush()
        else:
            self._target.write('\033[G' + progress_bar_str + percent_str)
            self._target.flush()

    @staticmethod
    def progress_bar_str(progress : float, width : int):
        # 0 <= progress <= 1
        progress = min(1, max(0, progress))
        whole_width = math.floor(progress * width)
        remainder_width = (progress * width) % 1
        part_width = math.floor(remainder_width * 8)
        part_char = [" ", "▏", "▎", "▍", "▌", "▋", "▊", "▉"][part_width]
        if (width - whole_width - 1) < 0:
          part_char = ""
        line = "[" + "█" * whole_width + part_char + " " * (width - whole_width - 1) + "]"
        return line
