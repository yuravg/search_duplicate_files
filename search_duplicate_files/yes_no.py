"""Show question and return answer
"""

import sys
import re


def yes_no(question, exact_answer=False):
    """Returns True if answer of questions is 'Yes'
    Function repeating until get answer Yes or No
    Keyword Arguments:
    question     -- question to show
    exact_answer -- exact answer requirement (allowed Y, y, N, n answer or
                    check answer by spell and case - only Yes No allowed)
    """
    if exact_answer:
        mask = ' (Yes/No)?'
    else:
        mask = ' (Y/N)?'
    while True:
        if sys.version_info[0] < 3:
            ans = raw_input(question + mask)
        else:
            ans = input(question + mask)
        if not exact_answer and re.match("y|Y|yes|Yes|YES", ans) or ans == 'Yes':
            result = True
            break
        elif not exact_answer and re.match("n|N|no|No|NO", ans) or ans == 'No':
            result = False
            break
        elif exact_answer:
            print("Allowed answers(check spell and case): 'Yes', 'No'")
    return result


if __name__ == '__main__':
    yes_no("First example, waiting simple answer")
    yes_no("Second example, waiting exact answer", True)
