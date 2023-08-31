import os


def main():


    x = os.environ['COMMIT_MSG']
    print(repr(x))


if __name__ == '__main__':
    main()