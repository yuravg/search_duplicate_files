"""
Remove directory
"""

import shutil
import os
import sys


def removetree(dirname):
    """Returns True id directory was deleted successfully
    Keyword Arguments:
    dirname  -- name of directory to remove
    """
    if dirname == '/':
        sys.exit("ERROR! Terrible directory name: '%s'" % dirname)
    try:
        if os.path.exists(dirname):
            shutil.rmtree(dirname)
        else:
            print("There are not directory: '%s'" % dirname)
        result = True
    except OSError:
        result = False
        print("Error! can't remove directory: '%s'" % dirname)
    return result


if __name__ == '__main__':
    def makedir(name):
        """make directory"""
        print('Make directory: %s' % name)
        if not os.path.isdir(name):
            os.makedirs(name)
    DIRNAME1 = 'tmp1'
    DIRNAME2 = 'tmp2'
    makedir(DIRNAME1)
    makedir(DIRNAME2)
    print('remove directory: %s' % DIRNAME1)
    removetree(DIRNAME1)
    print('remove directory: %s' % DIRNAME2)
    removetree(DIRNAME2)
    print('remove directory: %s' % "d:/HOME/tmp/temp_git/.git")
    PATH2DIR = 'd:/HOME/tmp/temp_git/.git'
    removetree(PATH2DIR)
