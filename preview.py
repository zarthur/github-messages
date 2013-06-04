#!/usr/bin/env python3

"""Convert message to array representing message in 3x3 font and display
it using matplotlib/pylab.
"""

import sys

import pylab

import fontify


def preview(message):
    """Diplay message in 3x3 font using pylab."""
    array = fontify.convert(message)
    pylab.spy(array)
    pylab.show()

if __name__ == '__main__':
    preview(' '.join(sys.argv[1:]))
