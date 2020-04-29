"""
Progress Bar
http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
"""

import time
import sys
from itertools import repeat


class ProgressBar(object):
    """Progress Bar
    Show progress bar in shell
    """
    def __init__(self, steps=100, bar_len=60, char_done='=', char_wait='-', msg=''):
        """
        Keyword Arguments:
        steps     -- steps for done progress bar
        bar_len   -- length of progress bar
        char_done -- char for done step
        char_wait -- char for wait step
        msg       -- bar message
        """
        self.__i = 0
        self.set_steps(steps)
        self.__bar_len = bar_len
        self.__char_done = char_done
        self.__char_wait = char_wait
        self.set_bar_message(msg)

    def set_steps(self, steps):
        """Set steps for progress bar"""
        self.__steps = steps

    def set_bar_message(self, msg):
        """Set message for progress bar
        """
        self.__msg = "%s    " % msg

    def show(self, counter_enable=True):
        """Show progress bar
        Keyword Arguments:
        counter_enable -- progress bar counter allowed
        """
        self.__progress_bar__(self.__i, self.__steps, self.__msg, self.__bar_len)
        if counter_enable:
            self.__i += 1

    def repeat_show(self, n):
        """Repeat show ProgressBar, n - times"""
        for _ in repeat(None, n):
            self.show()

    def __progress_bar__(self, count, steps, message='...', bar_len=60):
        filled_len = int(round(bar_len * count / float(steps)))
        percents = round(100.0 * count / float(steps), 1)
        bar = self.__char_done * filled_len + self.__char_wait * (bar_len - filled_len)
        if count == (steps-1):
            percents = 100
            bar = self.__char_done * bar_len
        sys.stdout.write('\r[%s] %s%s %s  ' % (bar, percents, '%', message))
        sys.stdout.flush()
        if count == (steps-1):
            print('')


if __name__ == '__main__':
    def run_progress_bar(steps=100, bar_len=60, char_done='=', char_wait='-', msg=''):
        pb = ProgressBar(steps, bar_len, char_done, char_wait, msg)
        for i in range(steps):
            time.sleep(0.01)
            pb.show()
    run_progress_bar()
    run_progress_bar(90, 30, '#', '-', "progress")
    run_progress_bar(100, 20, '*', '.', "Loading")
    steps = 100
    pb = ProgressBar(steps, 50, '+', '0')
    pb.set_bar_message('Initiate ...')
    for i in range(steps):
        time.sleep(0.01)
        pb.show()
