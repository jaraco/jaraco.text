import sys

from . import layouts

if __name__ == '__main__':
    layouts._translate_stream(sys.stdin, layouts.to_dvorak)
