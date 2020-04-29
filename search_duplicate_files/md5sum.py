"""
Calculate a file md5 checksum
"""

from __future__ import print_function
import sys
import hashlib
import os


def md5hex(fname):
    """Return md5 check sum (or False if can't calculate)
    Keyword Arguments:
    fname -- file name
    """
    hash_md5 = hashlib.md5()
    result = False
    try:
        with open(fname, "rb") as __f:
            for chunk in iter(lambda: __f.read(4096), b""):
                hash_md5.update(chunk)
            result = True
    except IOError as msg:
        sys.stderr.write("Can't open file, %s\n" % msg)
    if result:
        summary = hash_md5.hexdigest()
    else:
        summary = None
    return summary


if __name__ == '__main__':
    def calc_md5(fname):
        """get check sum to file"""
        csum = md5hex(fname)
        if csum:
            print('file: %s, md5 check sum (hex): %s' % (fname, csum))
    FNAME = os.path.basename(__file__)
    calc_md5(FNAME)
    FNAME = 'fname_not_exist.txt'
    calc_md5(FNAME)
