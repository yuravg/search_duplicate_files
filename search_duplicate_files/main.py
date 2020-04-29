"""Run point"""

import sys
import traceback
from .commandlinearg import get_args
from .search_duplicate_files import SearchDuplicateFiles
from .write_bash_completion import write_bash_completion
from .bash_completion import completion_data, completion_fname


def main():
    """Run point for the application script"""
    args = get_args()
    if args.mask == 'completion':
        write_bash_completion(completion_fname, completion_data)
    else:
        try:
            SearchDuplicateFiles(args)
        except KeyboardInterrupt:
            print("\nShutdown requested ... exiting")
        except Exception:
            traceback.print_exc(file=sys.stdout)
        sys.exit(0)
