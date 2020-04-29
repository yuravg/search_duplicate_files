"""
Work with files: copy, move, check file exist
"""

import os
import sys
import shutil
from .makedir import makedir


# http://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python
def copyfile(src, dst, override=False, verbosity=False):
    """Copy file
    Keyword Arguments:
    src       -- source file name
    dst       -- destination file name
    override  -- override file, if exist
    verbosity -- verbosity operation
    Return: True if operation successful
    """
    result = False
    if verbosity:
        print('Copy file: %s -> %s' % (src, dst))
    try:
        if os.path.exists(dst):
            if override:
                shutil.copy(src, dst)
                result = True
            else:
                print("Can't copy file: %s to %s, file already exist" % (src, dst))
        else:
            path = os.path.dirname(dst)
            if path != '':
                makedir(os.path.dirname(dst))
                shutil.copy(src, dst)
                result = True
    except Exception as e:
        print(e)
    return result


def file_exist(fname, verbosity=False, abort_and_exit=False):
    """Check if file exist
    Keyword Arguments:
    fname     -- file names
    verbosity -- verbosity operation
    Return: True if file exist
    """
    result = False
    try:
        if os.path.exists(fname):
            if os.path.isfile(fname):
                result = True
    except Exception as e:
        print(e)
    if verbosity:
        if not result:
            print("Can't open file: '%s'" % fname)
            if abort_and_exit:
                sys.exit("ERROR! Open file: '%s'\nExit from program!" % fname)
    return result


def movefile_vrb(src, dst, verbosity=False):
    """verbosity move file
    """
    if verbosity:
        print('Move file: %s -> %s' % (src, dst))
    shutil.move(src, dst)


def movefile(src, dst, override=False, add_index=False, verbosity=False):
    """Move or rename file
    Keyword Arguments:
    src       -- source file name
    dst       -- destination file name
    override  -- override file, if exist
    add_index -- add index to file name (only if files don't overrided)
    verbosity -- verbosity operation
    Return: True if operation successful
    """
    result = False
    try:
        if os.path.exists(dst):
            if override:
                os.remove(dst)
                movefile_vrb(src, dst, verbosity)
                result = True
            else:
                if add_index:
                    if not file_exist(dst):
                        movefile_vrb(src, dst, verbosity)
                        result = True
                    else:
                        path = os.path.dirname(dst)
                        extension = os.path.splitext(dst)[1]
                        fname = os.path.basename(dst)
                        fname_without_ext = os.path.splitext(fname)[0]
                        index = 'a'
                        while True:
                            new_fname = fname_without_ext + index + extension
                            new_path = os.path.join(path, new_fname)
                            if not file_exist(new_path):
                                movefile_vrb(src, new_path, verbosity)
                                result = True
                                break
                            index = chr(ord(index) + 1)
                else:
                    print("Can't move without override requpment: %s" % dst)
        else:
            movefile_vrb(src, dst, verbosity)
    except Exception as e:
        print(e)
    return result


if __name__ == '__main__':
    src_file = 'files.py'
    dst_file0 = 'files0.py'
    dst_file1 = 'tmp/files1.py'
    dst_file2 = 'tmp/files2.py'
    print('\nCopy file:')
    copyfile(src_file, dst_file1, True, True)
    print('\nCopy file without override:')
    copyfile(src_file, dst_file1, False, True)
    print('\nCopy file, override:')
    copyfile(src_file, dst_file1, True, True)
    print('')
    print('\nMove file:')
    copyfile(src_file, dst_file0, True, True)
    movefile(dst_file0, dst_file2, True, False, True)
    print('\nMove file without overide:')
    copyfile(src_file, dst_file0, True, True)
    movefile(dst_file0, dst_file2, True, False, True)
    copyfile(src_file, dst_file0, True, True)
    movefile(dst_file0, dst_file2, False, False, True)
    print('\nMove file with overide:')
    copyfile(src_file, dst_file0, True, True)
    movefile(dst_file0, dst_file2, True, False, True)
    copyfile(src_file, dst_file0, True, True)
    movefile(dst_file0, dst_file2, True, False, True)
    print('\nMove file with index adding:')
    copyfile(src_file, dst_file0, True, True)
    movefile(dst_file0, dst_file2, True, False, True)
    for i in range(3):
        copyfile(src_file, dst_file0, True, True)
        movefile(dst_file0, dst_file2, False, True, True)
