#!/usr/bin/env python

"""
Pandoc filter to convert all regular text to uppercase.

Code, link URLs, etc. are not affected.
"""

import re

from pandocfilters import Image, RawInline, toJSONFilter


def mdFilter(key, value, format, meta):
    """
    Filter datas.

    First part search for latex reference to figure and writes them
    as RawInline thereby backslashes are not escaped. It also removes
    the extra $ symbols.

    Second part search for images and set a label in the description
    in order to be able to make a reference to them.
    """
    if key == 'Str':
        if re.search("\$ref.*\$", value):
            # if we find a link, set it as raw link and re-add a
            # backslash before the ref keyword and remote
            value = value.replace("$", "")
            val = RawInline('latex', "\\" + value)
            return val

    if key == 'Image':
        [attrs, caption, src] = value
        # this means the image label hasn't been modified yet
        # (the mardown file doesn't come from a rst file)
        if caption[-1]['t'] != 'RawInline':
            new_capt = src[0]
            # add \label{IMAGE_LABEL} to the picture description
            new_desc = "\\" + "label{" + new_capt + "}"
            caption.append(RawInline('latex', new_desc))
            return Image(attrs, caption, src)


if __name__ == "__main__":
    toJSONFilter(mdFilter)
