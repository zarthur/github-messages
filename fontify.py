"""Convert given string to a numpy array using the 3x3 font encoding
found in font.yaml.

The github chart is roughly 52 * 7; removing the two end columns due to their
variable height given the day of the week, adding a row for spacing, allowing
each character to be 3x3 in size, and adding a column of space between
characters allows 24 characters.
"""

import numpy

from font33 import font


def _convert_row(message):
    array = [numpy.asarray(font[x]) for x in message]
    [x.resize((3, 3)) for x in array]

    # append whitespace after each character
    array = [numpy.concatenate((x, numpy.zeros((3, 1))), axis=1) for x in array]
    array = numpy.concatenate(array, axis=1)
    return array


def convert(message):
    """Convert message to a numpy array representing the message using
    the 3x3 font.
    """
    if len(message) > 24:
        raise RuntimeError('Input string must be at most 24 characters')

    message += ' ' * (24 - len(message))  # ensure message has 24 characters
    message = message.lower()
    separated = message[:12], message[12:]
    top_array, bottom_array = [_convert_row(row) for row in separated]
    middle = numpy.zeros((1, 48))
    end = numpy.zeros((7, 1))
    center = numpy.concatenate((top_array, middle, bottom_array), axis=0)
    array = numpy.concatenate((end, center, end), axis=1)
    return array
