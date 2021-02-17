from gui.objects.renderable import Renderable
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
class ProgressBar(Renderable):
    def __init__(self, progress_provider):
        super().__init__()
        self.progress_provider = progress_provider

    def render(self, renderer):
        progress = self.progress_provider()

        width = renderer.width - 1

        perc = int(progress * 100)
        perc_str = (str(perc).rjust(3) + " %")
        perc_str = perc_str.rjust(int((2+width+len(perc_str))/2))
        progress_bar = ProgressBar.progress_bar_str(progress, width)

        renderer.addstr(0, 0, progress_bar)
        renderer.addstr(1, 0, perc_str)

        return 2


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
