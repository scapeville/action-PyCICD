import os
import re
import sys


def parser(commit_msg):

    res = re.match(r'(?P<desc>.+?)[ ]*#(?P<type>r|t)[ ]*(?P<ver>\d+\.\d+\.\d+(b\d*)?)[ ]*$', commit_msg, re.IGNORECASE)
    if res is None:
        return None

    type = res.group('type').lower()
    ver = res.group('ver').lower()  # to make 1.0.0B -> 1.0.0b
    desc = res.group('desc')

    ## Checks
    if type == 'r':
        if 'b' in ver: raise AssertionError(f"The release version {repr(ver)} cannot be labeled as 'beta'.")
    if type == 't':
        if 'b' not in ver: raise AssertionError(f"The testing version {repr(ver)} must carry the label 'beta'.")

    return type, ver, desc


def main():

    res = parser(os.environ['COMMIT_MSG'])
    if res is None:
        print("Commit message didn't match the pattern.")
        sys.exit(0)
    else:
        type, ver, desc = res

    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        print(f'match=true', file=f)
        print(f'type={type}', file=f)
        print(f'ver={ver}', file=f)
        print(f'desc={desc}', file=f)


if __name__ == '__main__':
    main()