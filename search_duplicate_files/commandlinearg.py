"""Get arguments from command line
"""

try:
    from argparse import ArgumentParser, RawTextHelpFormatter
except ImportError:  # for version < 3.0
    from ArgParse import ArgumentParser, RawTextHelpFormatter

from .__init__ import __version__

__prog__ = "Search Duplicate Files"
__description__ = "Search, Show, Remove, Report Duplicate Files"
__version_string__ = '%s version %s' % (__prog__, __version__)
__epilog__ = "Example usage:\n\
Search way:\n\
1) without key     - duplicate by name and size\n\
2) --sum           - duplicate by name and md5sum\n\
3) --sum --no-name - duplicate by md5sum only (for any name under the mask)\n\
4) --no-size       - duplicate by name only\n\
5) --no-name       - duplicate by size only\n\
Delete/Move way:\n\
a) -d or -m        - interactive delete or move duplicate(after warning message)\n\
b) -d and -m (-md) - interactive move duplicate(after warning message),\n\
then request to delete directory with duplicate\n\
c) -d --no-i       - delete duplicate(after warning message), leave only the first found files"


def get_args():
    """Run Argument Parser and get argument from command line"""
    parser = ArgumentParser(prog=__prog__,
                            description=__description__,
                            epilog=__epilog__,
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument('mask',
                        nargs=None,
                        help="mask for search duplicate files(examples):\n\
1) .txt - simple mask\n\
2) '.jpg .txt .md' - complex mask(separeted by space)\n\
3) '' - all files\n\
(completion - to write bash completion file for this script)")
    parser.add_argument('--no-v', '--no-verbose', dest='verbose', action='store_false',
                        default=True,
                        help="Disable verbose output messages")
    parser.add_argument('-m', '--move', dest='move_en', action='store_true',
                        default=False,
                        help="Move duplicate files to temp directory")
    parser.add_argument('-d', '--delete', dest='delete_en', action='store_true',
                        default=False,
                        help="Delete duplicate files")
    parser.add_argument('-no-i', '--no-interactive', dest='interactive', action='store_false',
                        default=True,
                        help="Don't interactive delete/move operation\n\
(leave only the first found files)")
    parser.add_argument('--no-warning', dest='warning', action='store_false',
                        default=True,
                        help="Don't warning message before move or delete operation")
    parser.add_argument('-w', '--write-log', dest='write_log', action='store_true',
                        default=False,
                        help="Write log file")
    parser.add_argument('-p', '--path', dest='path', action='append',
                        default=[],
                        help="""Path to run search duplicate files\n\
(default - current directory), example usage: -p. -p../new_dir""")
    parser.add_argument('--no-size', dest='size_en', action='store_false',
                        default=True,
                        help="Don't compare files by size(mask for search only)")
    parser.add_argument('--no-name', dest='name_en', action='store_false',
                        default=True,
                        help="Don't compare files by name\
(mask for search by sum or size only)")
    parser.add_argument('-s', '--sum', dest='sum_en', action='store_true',
                        default=False,
                        help="Usage compare files by md5sum")
    parser.add_argument('-i', '--ignore-mask', dest='ignore_mask', action='append',
                        default=[],
                        help="Ignore mask or path, example usage: -i.git/ -i./tmp/ -iName")
    parser.add_argument('-a', '--show-arguments', dest='show_arguments', action='store_true',
                        default=False,
                        help="Write log file")
    parser.add_argument('-V', '--version',
                        action='version',
                        version=__version_string__)
    return parser.parse_args()
