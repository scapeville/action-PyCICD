import os
import re
import sys

## to make all subdirs under root dir importable
try:
    sys.path.append(os.environ['GITHUB_ACTION_PATH'])
except KeyError:  # Raised during testing
    sys.path.append(os.environ['GITHUB_WORKSPACE'])

from engine.constants import UPDATE_VER_MSG


def parser(commit_msg):
    """
    returns:
        - None           (if no match)
        - gate, payload  (if match)
    """

    ## 'call' commit
    res = re.match(r'(?P<desc>.+?)[ ]*#(?P<type>r|t)[ ]*(?P<ver>\d+\.\d+\.\d+(b\d*)?)[ ]*$', commit_msg, re.IGNORECASE)
    gate = 'call'

    ## 'auto' commit
    if res is None:
        res = re.match(rf'^{UPDATE_VER_MSG} #PyCICD-(?P<type>r|t)$', commit_msg, re.IGNORECASE)
        gate = 'auto'

    ## no pattern matched
    if res is None:
        return None


    ## Gating ##
    ##vvvvvvvv##

    if gate == 'call':
        ## Parsing
        type = res.group('type').lower()
        ver = res.group('ver').lower()  # to make 1.0.0B -> 1.0.0b
        desc = res.group('desc')
        ## Checks
        if (type == 'r') and ('b' in ver): raise AssertionError(f"The release version {repr(ver)} cannot be labeled as 'beta'.")
        if (type == 't') and ('b' not in ver): raise AssertionError(f"The testing version {repr(ver)} must carry the label 'beta'.")
        ## Loading the payload
        payload = [type, ver, desc]
        return gate, payload

    if gate == 'auto':
        ## Parsing
        type = res.group('type')
        ## Loading the payload
        payload = type
        return gate, payload


def main():
    """
    There are 2 types of commit messages that would continue the flow:
    - 'call' commit: This is the commit made by the users via pull request once they're done with the work.
    - 'auto' commit: This commit is done by the workflow once it's done updating the 'version' in pyproject.toml.

    If the commit message matches none of the above, the workflow is done and not continuing further.
    """

    commit_message = os.environ['commit_msg']
    print(f'DEBUG: commit_message: {repr(commit_message)}')

    ## Parse
    res = parser(commit_message)

    ## no-match gate
    if res is None:
        print("Commit message didn't match the pattern.")
        sys.exit(0)

    ## Unloading
    gate, payload = res


    ## Gating ##
    ##vvvvvvvv##

    if gate == 'call':
        type, ver, desc = payload
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            print(f'gate={gate}', file=f)
            print(f'type={type}', file=f)
            print(f'ver={ver}', file=f)
            print(f'desc={desc}', file=f)

    if gate == 'auto':
        type = payload
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            print(f'gate={gate}', file=f)
            print(f'type={type}', file=f)


if __name__ == '__main__':
    main()