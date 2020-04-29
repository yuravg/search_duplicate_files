"""
Make directory
"""

import os


def makedir(dir_name):
    """Make directory
    """
    try:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    except Exception as e:
        print("Error! can't create directory: %s" % e)


if __name__ == '__main__':
    makedir('test_dir_name')
