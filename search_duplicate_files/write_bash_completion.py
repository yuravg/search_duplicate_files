"""Write bash completion file
"""

from os.path import expanduser


def write_bash_completion(fname, data):
    """Write bash completion file
    File with Linux EOL
    Keyword Arguments:
    fname -- name of file which will be written to directory: '~.bash_completion.d/'
    data  -- auto-completion data
    """
    home = expanduser("~")
    fname = '%s/.bash_completion.d/%s' % (home, fname)
    print('')
    import sys
    if sys.version_info[0] < 3:
        f = open(fname, 'wb')
    else:
        f = open(fname, 'w', newline='\n')
    f.write(data)
    f.close()
    print('Write file: %s' % fname)
    print('\n* NOTE:')
    print('* to usage new bash completion file, run:')
    print("* '. %s'\n" % fname)


if __name__ == '__main__':
    d2file = '# Temp file:\n# writed by test script: write_bash_completion.py\n'
    f_name = 'test'
    write_bash_completion(f_name, d2file)
